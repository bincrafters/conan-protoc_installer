#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_installer
from bincrafters import build_shared


if __name__ == "__main__":
    docker_entry_script = ".ci/build.sh" if "docker_entry_script" in os.getenv("CONAN_DOCKER_IMAGE", "") else None
    arch = os.environ["ARCH"]
    builder = build_template_installer.get_builder(docker_entry_script=docker_entry_script)
    builder.add({"os" : build_shared.get_os(), "arch_build" : arch}, {}, {}, {})
    builder.run()
