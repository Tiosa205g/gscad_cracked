# 用于动态修改权限: 因为计算书等都是通过ini读取权限
import configparser
import time
import threading

paths = ["C:\\gscad\\steelize.ini", "C:\\Windows\\steelize.ini"]
is_wr = False


def write(cfg, path, encoding="utf-8"):
    try:
        with open(path, "w", encoding=encoding) as f:
            cfg.write(f)
    except PermissionError:
        print(f"权限不足,无法写入: {path}")
    except Exception as e:
        print(f"写入文件失败 {path}: {e}")


def wr_th(path: str):
    encodings = ["gbk", "gb2312", "utf-8", "latin-1"]
    config_encoding = None

    while True:
        try:
            # 首次运行时检测编码
            if config_encoding is None:
                for enc in encodings:
                    try:
                        config = configparser.ConfigParser()
                        config.read(path, encoding=enc)
                        config_encoding = enc
                        print(f"检测到编码: {path} 使用 {enc}")
                        break
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        continue
                if config_encoding is None:
                    print(f"无法识别 {path} 的编码")
                    time.sleep(0.5)
                    continue
            else:
                config = configparser.ConfigParser()
                config.read(path, encoding=config_encoding)

            is_modified = False
            for item in config["User"].items():
                if item[1] == "3":
                    is_modified = True
                    config.set("User", item[0], "9999")
                elif item[1] == "0":
                    is_modified = True
                    config.set("User", item[0], "1")
            if is_modified:
                write(config, path, config_encoding)
                print(f"\n已修改: {path}")
        except KeyError:
            print(f"配置文件 {path} 中未找到 [User] 节")
        except Exception as e:
            print(f"处理 {path} 时出错: {e}")
        time.sleep(0.5)  # 500ms一次检测


if __name__ == "__main__":
    for path in paths:
        t = threading.Thread(target=wr_th, args=(path,), daemon=True)
        t.start()
    is_run = True
    while is_run:
        is_run = False if input("输入q退出\n") == "q" else True

    exit(0)
