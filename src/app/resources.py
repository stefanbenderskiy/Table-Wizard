class Resources:
    dirs = {
        "root": "../../res",
        "res": "../../res",
        "ui": "../../res/ui",
        "imgs": "../../res/imgs",
    }

    @staticmethod
    def get_resource(dirname, filename):
        return Resources.dirs[dirname] + "/" + filename

    @staticmethod
    def get_ui(filename):
        return Resources.get_resource("ui", filename)

