# 用于动态修改权限: 因为计算书等都是通过ini读取权限
import configparser
import time
import threading

paths = ["C:\\gscad\\steelize.ini", "C:\\Windows\\steelize.ini"]
is_wr = False


def write(cfg, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            cfg.write(f)
    except PermissionError:
        print(f"权限不足,无法写入: {path}")
    except Exception as e:
        print(f"写入文件失败 {path}: {e}")


def wr_th(path: str):
    while True:
        try:
            config = configparser.ConfigParser()
            config.read(path, encoding="utf-8")
            is_modified = False
            for item in config["User"].items():
                if item[1] == "3":
                    is_modified = True
                    config.set("User", item[0], "9999")
                elif item[1] == "0":
                    is_modified = True
                    config.set("User", item[0], "1")
            if is_modified:
                write(config, path)
                print(f"\n已修改: {path}")
        except KeyError:
            print(f"配置文件 {path} 中未找到 [User] 节")
        except FileNotFoundError:
            print(f"配置文件不存在: {path}")
        except Exception as e:
            print(f"处理 {path} 时出错: {e}")
        time.sleep(0.5)  # 500ms一次检测


if __name__ == "__main__":
    for path in paths:
        t = threading.Thread(target=wr_th, args=(path,), daemon=True)
        t.start()
    is_run = True
    while is_run:
        is_run = False if input("输入q退出:") == "q" else True

    exit(0)
