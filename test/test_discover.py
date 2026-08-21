import pytest

from reqtrace.core.discover import find_packages
from reqtrace.core.models import PackageType


@pytest.fixture
def python_project(tmp_path):
    project = tmp_path / "python_project"
    tests = project / "tests"
    tests.mkdir(parents=True)

    (project / "pyproject.toml").write_text(
        "[project]\n"
        'name = "python-project"\n'
    )
    (project / "REQUIREMENTS.md").write_text(
        "# Requirements\n"
    )
    (tests / "test_example.py").write_text(
        "def test_example():\n"
        "    assert True\n"
    )

    return tmp_path


@pytest.fixture
def ros_project(tmp_path):
    project = tmp_path / "ros_project"
    tests = project / "tests"
    tests.mkdir(parents=True)

    (project / "package.xml").write_text(
        "<package></package>\n"
    )
    (project / "REQUIREMENTS.md").write_text(
        "# Requirements\n"
    )
    (tests / "test_example.py").write_text(
        "def test_example():\n"
        "    assert True\n"
    )

    return tmp_path


def test_find_python_project(python_project):
    packages = find_packages(python_project)

    assert len(packages) == 1

    package = packages[0]
    assert package.root == python_project / "python_project"
    assert package.package_path == python_project / "python_project" / "pyproject.toml"
    assert package.package_type == PackageType("pyproject.toml")
    assert package.requirements_md == [
        python_project / "python_project" / "REQUIREMENTS.md"
    ]


def test_find_ros_project(ros_project):
    packages = find_packages(ros_project)

    assert len(packages) == 1

    package = packages[0]
    assert package.root == ros_project / "ros_project"
    assert package.package_path == ros_project / "ros_project" / "package.xml"
    assert package.package_type == PackageType("package.xml")
    assert package.requirements_md == [
        ros_project / "ros_project" / "REQUIREMENTS.md"
    ]