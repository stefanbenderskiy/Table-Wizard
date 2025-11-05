root = "../.."
res = f"{root}/res"
class Resources:
    dirs = {
        "root": root,
        "res": res,
        "ui": f"{res}/ui",
        "image": f"{res}/imgs",
    }

    @staticmethod
    def get_resource(dirname, filename):
        return Resources.dirs[dirname] + "/" + filename

    @staticmethod
    def get_ui(filename):
        return Resources.get_resource("ui", filename)

