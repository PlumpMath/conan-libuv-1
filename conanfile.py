from conans import ConanFile, tools, ConfigureEnvironment
import os


class LibuvConan(ConanFile):
    name = "LibUV"
    version = "1.9.1"
    settings = "os", "compiler", "build_type", "arch"
    # No exports necessary

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
        self.run("cd libuv-v1.9.1 && make -j %s" % concurrency)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["uv"]
