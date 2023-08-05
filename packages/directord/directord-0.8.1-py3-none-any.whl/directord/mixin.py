#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import getpass
import json
import multiprocessing
import os
import sys

from distutils import util as dist_utils

import jinja2
from jinja2 import StrictUndefined

import yaml

import directord

from directord import logger
from directord import utils


class Mixin:
    """Mixin class."""

    def __init__(self, args):
        """Initialize the Directord mixin.

        Sets up the mixin object.

        :param args: Arguments parsed by argparse.
        :type args: Object
        """

        self.args = args
        self.blueprint = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            keep_trailing_newline=True,
            undefined=StrictUndefined,
        )
        self.log = logger.getLogger(
            name="directord", debug_logging=getattr(args, "debug", False)
        )

    def format_action(
        self,
        verb,
        execute,
        arg_vars=None,
        targets=None,
        ignore_cache=False,
        restrict=None,
        parent_id=None,
        parent_sha3_224=None,
        return_raw=False,
        parent_async=False,
    ):
        """Return a JSON encode object for task execution.

        While formatting the message, the method will treat each verb as a
        case and parse the underlying sub-command, formatting the information
        into a dictionary.

        :param verb: Action to parse.
        :type verb: String
        :param execute: Execution string to parse.
        :type execute: String
        :param targets: Target argents to send job to.
        :type targets: List
        :param arg_vars: Argument dictionary, used to set arguments in
                         dictionary format instead of string format.
        :type arg_vars: Dictionary
        :param ignore_cache: Instruct the entire execution to
                             ignore client caching.
        :type ignore_cache: Boolean
        :param restrict: Restrict job execution based on a provided task
                         SHA3_224.
        :type restrict: List
        :param parent_id: Set the parent UUID for execution jobs.
        :type parent_id: String
        :param parent_sha3_224: Set the parent sha3_224 for execution jobs.
        :type parent_id: String
        :param return_raw: Enable a raw return from the server.
        :type return_raw: Boolean
        :param parent_async: Enable a parent job to run asynchronously.
        :type parent_async: Boolean
        :returns: String
        """

        data = dict(verb=verb)
        self.log.debug("Executing - VERB:%s, EXEC:%s", verb, execute)
        component_kwargs = dict(
            exec_array=execute, data=data, arg_vars=arg_vars
        )

        success, transfer, component = directord.component_import(
            component=verb.lower(),
            job_id=parent_id,
        )
        if not success:
            raise SystemExit(component)

        setattr(component, "verb", verb)
        data.update(component.server(**component_kwargs))

        data["timeout"] = getattr(component.known_args, "timeout", 600)
        data["run_once"] = getattr(component.known_args, "run_once", False)
        data["task_sha3_224"] = utils.object_sha3_224(obj=data)
        data["return_raw"] = return_raw
        data["skip_cache"] = ignore_cache or getattr(
            component.known_args, "skip_cache", False
        )

        if targets:
            data["targets"] = targets

        if parent_async:
            data["parent_async"] = parent_async

        if parent_id:
            data["parent_id"] = parent_id

        if parent_sha3_224:
            data["parent_sha3_224"] = parent_sha3_224

        if restrict:
            data["restrict"] = restrict

        if transfer:
            job = {
                "jobs": [
                    {"WORKDIR": "/etc/directord/components"},
                    {
                        "ADD": "{} {}".format(
                            transfer, "/etc/directord/components/"
                        )
                    },
                ]
            }
            self.exec_orchestrations(
                orchestrations=[job],
                defined_targets=data.get("targets"),
                return_raw=True,
            )

        return json.dumps(data)

    def exec_orchestrations(
        self,
        orchestrations,
        defined_targets=None,
        restrict=None,
        ignore_cache=False,
        return_raw=False,
    ):
        """Execute orchestration jobs.

        Iterates over a list of orchestartion blobs, fingerprints the jobs,
        and then runs them.

        :param orchestrations: List of Dictionaries which are run as
                               orchestartion.
        :type orchestrations: List
        :param defined_targets: List of targets to limit a given execution to.
                                This target list provides an override for
                                targets found within a given orchestation.
        :type defined_targets: List
        :param restrict: Restrict a given orchestration job to a set of
                         SHA3_224 job fingerprints.
        :type restrict: Array
        :param ignore_cache: Instruct the orchestartion job to ignore cached
                             executions.
        :type ignore_cache: Boolean
        :param return_raw: Enable a raw return from the server.
        :type return_raw: Boolean
        :returns: List
        """

        job_to_run = list()
        for orchestrate in orchestrations:
            parent_sha3_224 = utils.object_sha3_224(obj=orchestrate)
            parent_id = utils.get_uuid()
            targets = defined_targets or orchestrate.get("targets", list())
            try:
                parent_async = bool(
                    dist_utils.strtobool(orchestrate.get("async", "False"))
                )
            except (ValueError, AttributeError):
                parent_async = bool(orchestrate.get("async", False))
            jobs = orchestrate["jobs"]
            for job in jobs:
                arg_vars = job.pop("vars", None)
                key, value = next(iter(job.items()))
                job_to_run.append(
                    dict(
                        verb=key,
                        execute=[value],
                        arg_vars=arg_vars,
                        targets=targets,
                        restrict=restrict,
                        ignore_cache=ignore_cache,
                        parent_id=parent_id,
                        parent_sha3_224=parent_sha3_224,
                        return_raw=return_raw,
                        parent_async=parent_async,
                    )
                )

        return_data = list()
        if getattr(self.args, "finger_print", False):
            count = 0
            for job in job_to_run:
                tabulated_data = list()
                formatted_job = self.format_action(**job)
                item = json.loads(formatted_job)
                exec_str = " ".join(job["execute"])
                if len(exec_str) >= 30:
                    exec_str = "{execute}...".format(execute=exec_str[:27])
                tabulated_data.extend(
                    [
                        count,
                        job["parent_sha3_224"],
                        item["verb"],
                        exec_str,
                        item["task_sha3_224"],
                    ]
                )
                return_data.append(tabulated_data)
                count += 1
            utils.print_tabulated_data(
                data=return_data,
                headers=["count", "parent_sha", "verb", "exec", "job_sha"],
            )
            return []
        else:
            for job in job_to_run:
                formatted_job = self.format_action(**job)
                return_data.append(
                    directord.send_data(
                        socket_path=self.args.socket_path, data=formatted_job
                    )
                )

        return return_data

    def run_orchestration(self):
        """Run orchestration jobs.

        When orchestration jobs are executed the files are organized and
        then indexed. Once indexed, the jobs are sent to the server. send
        returns are captured and returned on method exit.

        :returns: List
        """

        return_data = list()
        for orchestrate_file in self.args.orchestrate_files:
            orchestrate_file = os.path.abspath(
                os.path.expanduser(orchestrate_file)
            )
            if not os.path.exists(orchestrate_file):
                raise FileNotFoundError(
                    "The [ {} ] file was not found.".format(orchestrate_file)
                )
            else:
                with open(orchestrate_file) as f:
                    orchestrations = yaml.safe_load(f)

                if self.args.target:
                    defined_targets = list(set(self.args.target))
                else:
                    defined_targets = list()

                return_data.extend(
                    self.exec_orchestrations(
                        orchestrations=orchestrations,
                        defined_targets=defined_targets,
                        restrict=self.args.restrict,
                        ignore_cache=self.args.ignore_cache,
                        return_raw=getattr(self.args, "poll", False),
                    )
                )
        else:
            return return_data

    def run_exec(self):
        """Execute an exec job.

        Jobs are parsed and then sent to the server for processing. All return
        items are captured in an array which is returned on method exit.

        :returns: List
        """

        format_kwargs = dict(
            verb=self.args.verb,
            execute=self.args.exec,
            return_raw=getattr(self.args, "poll", False),
        )
        if self.args.target:
            format_kwargs["targets"] = list(set(self.args.target))

        return [
            directord.send_data(
                socket_path=self.args.socket_path,
                data=self.format_action(**format_kwargs),
            )
        ]

    def return_tabulated_info(self, data):
        """Return a list of data that will be tabulated.

        :param data: Information to generally parse and return
        :type data: Dictionary
        :returns: List
        """

        tabulated_data = [["ID", self.args.job_info]]
        for key, value in data.items():
            if not value:
                continue

            if key.startswith("_"):
                continue

            if key == "PROCESSING":
                if value == b"\026":
                    value = "True"
                else:
                    value = "False"

            if isinstance(value, list):
                value = "\n".join(value)
            elif isinstance(value, dict):
                value = "\n".join(
                    ["{} = {}".format(k, v) for k, v in value.items() if v]
                )

            tabulated_data.append([key.upper(), value])
        else:
            return tabulated_data

    def return_tabulated_data(self, data, restrict_headings):
        """Return tabulated data displaying a limited set of information.

        :param data: Information to generally parse and return
        :type data: Dictionary
        :param restrict_headings: List of headings in string format to return
        :type restrict_headings: List
        :returns: List
        """

        def _computed_totals(item, value_heading, value):
            if item not in seen_computed_key:
                if isinstance(value, bool):
                    bool_heading = "{}_{}".format(value_heading, value).upper()
                    if bool_heading in computed_values:
                        computed_values[bool_heading] += 1
                    else:
                        computed_values[bool_heading] = 1
                elif isinstance(value, (float, int)):
                    if value_heading in computed_values:
                        computed_values[value_heading] += value
                    else:
                        computed_values[value_heading] = value

        tabulated_data = list()
        computed_values = dict()
        seen_computed_key = list()
        found_headings = ["ID"]
        original_data = list(dict(data).items())
        result_filter = getattr(self.args, "filter", None)
        for key, value in original_data:
            arranged_data = [key]
            include = result_filter is None
            for item in restrict_headings:
                if item not in found_headings:
                    found_headings.append(item)
                if item.upper() not in value and item.lower() not in value:
                    arranged_data.append(0)
                else:
                    try:
                        report_item = value[item.upper()]
                    except KeyError:
                        report_item = value[item.lower()]

                    if item.upper() == "PROCESSING":
                        if report_item.encode() == b"\026":
                            report_item = "True"
                            if result_filter == "processing":
                                include = True
                        else:
                            report_item = "False"
                    elif (
                        isinstance(report_item, list) and len(report_item) > 0
                    ):
                        if (
                            result_filter == "success"
                            and item.upper() == "SUCCESS"
                        ):
                            include = True
                        if (
                            result_filter == "failed"
                            and item.upper() == "FAILED"
                        ):
                            include = True

                    if not report_item:
                        arranged_data.append(0)
                    else:
                        if report_item and isinstance(report_item, list):
                            arranged_data.append(len(report_item))
                        elif isinstance(report_item, float):
                            arranged_data.append("{:.2f}".format(report_item))
                        else:
                            arranged_data.append(report_item)
                        _computed_totals(
                            item=key, value_heading=item, value=report_item
                        )

            if include:
                seen_computed_key.append(key)
                tabulated_data.append(arranged_data)

        return tabulated_data, found_headings, computed_values

    @staticmethod
    def bootstrap_catalog_entry(entry):
        """Return a flattened list of bootstrap job entries.

        :param entry: Catalog entry for bootstraping.
        :type entry: Dictionary
        :returns: List
        """

        ordered_entries = list()
        for item in ["jobs", "targets"]:
            if item not in entry:
                raise SystemExit(
                    "The bootstrap catalog is missing a"
                    " required component: {}".format(item)
                )

        args = entry.get("args", dict(port=22, username=getpass.getuser()))
        for target in entry["targets"]:
            try:
                target_host = target["host"]
            except KeyError:
                raise SystemExit("[host] is undefined in bootstrap catalog")
            item = dict(
                host=target_host,
                username=target.get(
                    "username", args.get("username", getpass.getuser())
                ),
                port=target.get("port", args.get("port", 22)),
                jobs=entry["jobs"],
            )
            ordered_entries.append(item)
        return ordered_entries

    @staticmethod
    def bootstrap_localfile_padding(localfile):
        """Return a padded localfile.

        Local files should be a fully qualified path. If the path is
        not fully qualified, this method will add the tools prefix to the
        file.

        :param localfile: Path to file.
        :type localfile: String
        :returns: String
        """

        if not localfile.startswith(os.sep):
            if sys.prefix == sys.base_prefix:
                base_path = os.path.join(
                    sys.base_prefix, "share/directord/tools"
                )
            else:
                base_path = os.path.join(sys.prefix, "share/directord/tools")
            return os.path.join(base_path, localfile)

        return localfile

    def bootstrap_flatten_jobs(self, jobs, return_jobs=None):
        """Return a flattened list of jobs.

        This method will flatten a list of jobs, and if an entry is an array
        the method will recurse.

        :param jobs: List of jobs to parse.
        :type jobs: List
        :param return_jobs: Seed list to use when flattening the jobs array.
        :type: return_jobs: None|List
        :returns: List
        """

        if not return_jobs:
            return_jobs = list()

        for job in jobs:
            if isinstance(job, list):
                return_jobs = self.bootstrap_flatten_jobs(
                    jobs=job, return_jobs=return_jobs
                )
            else:
                return_jobs.append(job)

        return return_jobs

    def bootstrap_run(self, job_def, catalog):
        """Run a given set of jobs using a defined job definition.

        This method requires a job definition which contains the following.

        {
            "host": String,
            "port": Integer,
            "username": String,
            "key_file": String,
            "jobs": List,
        }

        :param jobs_def: Defined job definition.
        :type jobs_def: Dictionary
        :param catalog: The job catalog definition.
        :type catalog: Dictionary
        """

        self.log.info("Running bootstrap for %s", job_def["host"])
        for job in self.bootstrap_flatten_jobs(jobs=job_def["jobs"]):
            key, value = next(iter(job.items()))
            self.log.debug("Executing: %s %s", key, value)
            with utils.SSHConnect(
                host=job_def["host"],
                username=job_def["username"],
                port=job_def["port"],
                key_file=job_def.get("key_file"),
                debug=getattr(self.args, "debug", False),
            ) as ssh:
                if key == "RUN":
                    self.bootstrap_exec(
                        ssh=ssh, command=value, catalog=catalog
                    )
                elif key == "ADD":
                    localfile, remotefile = value.split(" ", 1)
                    localfile = self.bootstrap_localfile_padding(localfile)
                    self.bootstrap_file_send(
                        ssh=ssh, localfile=localfile, remotefile=remotefile
                    )
                elif key == "GET":
                    remotefile, localfile = value.split(" ", 1)
                    self.bootstrap_file_get(
                        ssh=ssh, localfile=localfile, remotefile=remotefile
                    )

    def bootstrap_file_send(self, ssh, localfile, remotefile):
        """Run a remote put command.

        :param ssh: SSH connection object.
        :type ssh: Object
        :param localfile: Local file to transfer.
        :type localfile: String
        :param remotefile: Remote file destination.
        :type remotefile: String
        """

        fileinfo = os.stat(localfile)
        chan = ssh.session.scp_send64(
            remotefile,
            fileinfo.st_mode & 0o777,
            fileinfo.st_size,
            fileinfo.st_mtime,
            fileinfo.st_atime,
        )
        self.log.debug(
            "channel: %s, local file: %s, remote file: %s",
            chan,
            localfile,
            remotefile,
        )
        with open(localfile, "rb") as local_fh:
            for data in local_fh:
                chan.write(data)

    @staticmethod
    def bootstrap_file_get(ssh, localfile, remotefile):
        """Run a remote get command.

        :param ssh: SSH connection object.
        :type ssh: Object
        :param localfile: Local file destination.
        :type localfile: String
        :param remotefile: Remote file to transfer.
        :type remotefile: String
        """

        chan, _ = ssh.session.scp_recv2(remotefile)
        with open(localfile, "wb") as f:
            while True:
                size, data = chan.read()
                f.write(data)
                if size > 0:
                    break

    def bootstrap_exec(self, ssh, command, catalog):
        """Run a remote command.

        Run a command and check the status. If there's a failure the
        method will exit error.

        :param session: SSH Session connection object.
        :type session: Object
        :param command: Plain-text execution string.
        :type command: String
        :param catalog: The job catalog definition.
        :type catalog: Dictionary
        """

        ssh.open_channel()
        t_command = self.blueprint.from_string(command)
        ssh.channel.execute(t_command.render(**catalog))
        ssh.channel.wait_eof()
        ssh.channel.close()
        ssh.channel.wait_closed()

        if ssh.channel.get_exit_status() != 0:
            size, data = ssh.channel.read()
            while size > 0:
                size, _data = ssh.channel.read()
                data += _data
            print(
                "{line} Start Error Information {line}".format(line=("=" * 10))
            )
            try:
                data = data.decode()
            except AttributeError:
                pass
            print(data)
            print(
                "{line} End Error Information {line}".format(line=("=" * 10))
            )
            raise SystemExit("Bootstrap command failed: {}".format(command))

    def bootstrap_q_processor(self, queue, catalog):
        """Run a queing execution thread.

        The queue will be processed so long as there are objects to process.

        :param queue: SSH connection object.
        :type queue: Object
        :param catalog: The job catalog definition.
        :type catalog: Dictionary
        """

        while True:
            try:
                job_def = queue.get(timeout=3)
            except Exception:
                break
            else:
                self.bootstrap_run(
                    job_def=job_def,
                    catalog=catalog,
                )

    def bootstrap_cluster(self):
        """Run a cluster wide bootstrap using a catalog file.

        Cluster bootstrap requires a catalog file to run. Catalogs are broken
        up into two sections, `directord_server` and `directord_client`. All
        servers are processed serially and first. All clients are processing
        in parallel using a maximum of the threads argument.
        """

        q = multiprocessing.Queue()
        catalog = dict()
        if not self.args.catalog:
            raise SystemExit("No catalog was defined.")

        for c in self.args.catalog:
            utils.merge_dict(base=catalog, new=yaml.safe_load(c))

        directord_server = catalog.get("directord_server")
        if directord_server:
            self.log.info("Loading server information")
            for s in self.bootstrap_catalog_entry(entry=directord_server):
                s["key_file"] = self.args.key_file
                self.bootstrap_run(job_def=s, catalog=catalog)

        directord_clients = catalog.get("directord_clients")
        if directord_clients:
            self.log.info("Loading client information")
            for c in self.bootstrap_catalog_entry(entry=directord_clients):
                c["key_file"] = self.args.key_file
                q.put(c)

        cleanup_threads = list()
        for _ in range(self.args.threads):
            t = multiprocessing.Process(
                target=self.bootstrap_q_processor, args=(q, catalog)
            )
            t.daemon = True
            t.start()
            cleanup_threads.append(t)

        for t in cleanup_threads:
            t.join()
