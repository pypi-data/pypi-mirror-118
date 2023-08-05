import argparse
import sys
import subprocess
import shutil
from pathlib import Path

# try:
#    from kwik import __version__
# except:
#    __version__ = "unknown"

__version__ = "unknown"

PIP_INSTALL = [sys.executable, "-m", "pip", "install"]


def run_server(working_dir, args):
    pass


def run_tests(working_dir, args):
    pass


def create_app(working_dir, args):
    pass


def cleanup(working_dir: Path):
    remove_folders = [working_dir.joinpath("build"), working_dir.joinpath("dist")]
    remove_folders += [x for x in working_dir.glob("**/__pycache__") if x.is_dir()]
    remove_folders += [x for x in working_dir.glob("**/*.egg-info") if x.is_dir()]
    for folder in remove_folders:
        if folder.exists():
            print(f"Removing: {folder}")
            shutil.rmtree(folder, ignore_errors=True)


def refresh(working_dir: Path, args):
    cleanup(working_dir)


def build(working_dir: Path, args):
    if working_dir.joinpath("setup.py").exists():
        if args.clean:
            # clean build
            cleanup(working_dir)

        if not args.no_update:
            # update build dependencies
            subprocess.check_call(PIP_INSTALL + ["--upgrade", "pip", "build"])
            subprocess.check_call(PIP_INSTALL + ["wheel"])  # "bdist_wheel"

        subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"])
        subprocess.check_call([sys.executable, "-m", "build"])
        return

    else:
        print(
            f"No setup.py file found in the current directory: { working_dir }\n"
            f"Run build command from the project root directory with a setup.py file."
        )
        return


def deploy(working_dir: Path, args):
    if working_dir.joinpath("dist").exists():
        if not args.no_update:
            # update deploy dependencies
            subprocess.check_call(PIP_INSTALL + ["--upgrade", "twine"])
        if args.test:
            repo = "testpypi"
        else:
            repo = "pypi"

        subprocess.check_call(
            [sys.executable, "-m", "twine", "upload", "--repository", repo, "dist/*"]
        )
    else:
        print(
            f"No dist folder found in the current directory: { working_dir }\n"
            f"Run deploy command from the project root directory with a dist directory."
        )
        return


def main():
    working_dir = Path.cwd()
    parser = argparse.ArgumentParser(prog="kwik", description="kwik cli")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"kwik { __version__ }",
        help="Display the current version number.",
    )

    subparsers = parser.add_subparsers()

    # build subcommand
    # kwik build
    build_parser = subparsers.add_parser("build", help="Build commands")
    build_parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Create a clean build, defaults to false.",
    )
    build_parser.add_argument(
        "--no-update",
        action="store_true",
        dest="no_update",
        help="Do not attempt to update build dependencies; defaults to false, i.e. default behavior is to update dependencies.",
    )
    build_parser.set_defaults(func=build)

    # kwik deploy
    deploy_parser = subparsers.add_parser("deploy", help="Deploy commands")
    deploy_parser.add_argument(
        "--test",
        action="store_true",
        dest="test",
        help="Deploy to test repository, defaults to false.",
    )
    deploy_parser.add_argument(
        "--no-update",
        action="store_true",
        dest="no_update",
        help="Do not attempt to update deploy dependencies; defaults to false, i.e. default behavior is to update dependencies.",
    )
    deploy_parser.set_defaults(func=deploy)

    # kwik refresh
    refresh_parser = subparsers.add_parser("refresh", help="Refresh project folder")
    refresh_parser.set_defaults(func=refresh)

    # run subcommand
    # kwik run
    # kwik run tests
    # kwik run server
    run_parser = subparsers.add_parser("run", help="Run commands")
    run_subparsers = run_parser.add_subparsers()

    # kwik run tests
    # kwik run tests -a someapp
    # kwik run tests --app someapp
    run_tests_parser = run_subparsers.add_parser("tests", help="run test suite")
    run_tests_parser.add_argument(
        "-a", "--app", type=str, help="Application name to run tests"
    )

    run_tests_parser.set_defaults(func=run_tests)

    # kwik run server
    # kwik run server -p 8080
    # kwik run server --port 8080
    run_server_parser = run_subparsers.add_parser("server", help="Run the server")
    run_server_parser.add_argument(
        "-p",
        "--port",
        metavar="<int:port>",
        type=int,
        help="Port number to run the server on",
    )
    run_server_parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        default=False,
        help="Open the url in browser",
    )
    run_server_parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        default=False,
        help="Copy the url to clipboard",
    )
    run_server_parser.set_defaults(func=run_server)

    # create subcommand
    # kwik create app
    create_parser = subparsers.add_parser("create", help="Create")
    create_subparsers = create_parser.add_subparsers()
    create_app_parser = create_subparsers.add_parser("app", help="Create a new app")
    create_app_parser.add_argument(
        "-n", "--name", dest="app_name", type=str, help="create an app template"
    )
    create_app_parser.set_defaults(func=create_app)

    args = parser.parse_args()
    args.func(working_dir, args)
    # print(working_dir)
    # print(args)
    # print(args.func.__name__)
    # func = args.func
    # args.func(working_dir, args)


if __name__ == "__main__":
    main()
