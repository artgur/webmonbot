def test_packages(host):
    packages = [
        "epel-release",
        "python34",
        "python34-requests"
    ]
    for package in packages:
        assert host.package(package).is_installed


def test_config(host):
    assert host.file("/etc/webmonbot.json").is_file


def test_service(host):
    assert host.service("webmonbot").is_running