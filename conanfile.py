from conans import ConanFile, tools, ConfigureEnvironment
import os


class LibuvConan(ConanFile):
    name = "LibUV"
    description = "LibUV asynchronous I/O framework"
    version = "1.9.1"
    license = "Apache Software License 2.0"
    author = "Kyle Downey"
    url = "https://github.com/kyle-downey/conan-libuv"

    settings = {
        "os": ["Linux", "Macos"],
        "compiler": None,
        "build_type": None,
        "arch": None
    }

    def source(self):
        tools.download("http://dist.libuv.org/dist/v1.9.1/libuv-v1.9.1.tar.gz", "libuv.tgz")
        tools.untargz("libuv.tgz")
        os.unlink("libuv.tgz")

    def build(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)

        concurrency = 1
        try:
            import multiprocessing
            concurrency = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass

        self.run("chmod +x libuv-v1.9.1/autogen.sh")
        self.run("cd libuv-v1.9.1 && ./autogen.sh")

        args = []

        self.run("chmod +x libuv-v1.9.1/configure")
        self.run("cd libuv-v1.9.1 && %s ./configure %s" % (env.command_line, ' '.join(args)))

        cppflags = ""
        if self.settings.os == "Linux":
            cppflags = "CPPFLAGS=-fPIC "
        self.run("cd libuv-v1.9.1 && make " + cppflags + "-j %s" % concurrency)

    def package(self):
        self.copy("*.h", dst="include", src="libuv-v1.9.1/include", keep_path=False)
        self.copy("*.*", dst="lib", src="libuv-v1.9.1/.libs", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["uv"]
