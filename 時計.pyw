import datetime
import tkinter as tk
import ctypes
import math


class Clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.windowWidth = 900
        self.windowHeight = 900
        self.canvasWidth = 800
        self.canvasHeight = 800
        self.origin = {"x": self.canvasWidth / 2, "y": self.canvasHeight / 2} # 原点の座標
        self.hour = {"time": 0, "length": 200, "x": 0, "y": 0} # 時刻, 針の長さ, x座標, y座標
        self.minute = {"time": 0, "length": 300, "x": 0, "y": 0}
        self.second = {"time": 0, "length": 320, "x": 0, "y": 0}
        self.label = tk.Label()
        self.canvas = tk.Canvas(
            self.master, width=self.canvasWidth, height=self.canvasHeight, cursor="star")
        self.canvas.pack()

        master.geometry(f"{self.windowWidth}x{self.windowHeight}")
        master.title("時計")

        self.drawBackground()
    
    def drawBackground(self):
        for measure in range(60):
            measureX1 = (
                self.second["length"] - 15) * math.cos(math.radians(90 - measure * 6))
            measureX2 = self.second["length"] * math.cos(math.radians(90 - measure * 6))
            measureY1 = (
                self.second["length"] - 15) * math.sin(math.radians(90 - measure * 6))
            measureY2 = self.second["length"] * math.sin(math.radians(90 - measure * 6))

            measureX1 = self.origin["x"] + measureX1 #座標を変換
            measureX2 = self.origin["x"] + measureX2
            measureY1 = self.canvasHeight - (self.origin["y"] + measureY1)
            measureY2 = self.canvasHeight - (self.origin["y"] + measureY2)

            if not math.floor(measure % 5):
                lineColor = "#19448e"
                lineWidth = 10
            else:
                lineColor = "#705b67"
                lineWidth = 3
            self.canvas.create_line(
            measureX1, measureY1, measureX2, measureY2,
            fill=lineColor, width=lineWidth, tag="background")

    def getTime(self):
        currentTime = datetime.datetime.now()
        self.hour["time"] = currentTime.hour
        self.minute["time"] = currentTime.minute
        self.second["time"] = currentTime.second

    def CalcCoordinate(self):
        # x = length * cosθ
        # y = length * sinθ
        self.hour["x"] = self.hour["length"] * math.cos(
            math.radians(90 - (self.hour["time"] * 30 + self.minute["time"] * 0.5)))
        self.hour["y"] = self.hour["length"] * math.sin(
            math.radians(90 - (self.hour["time"] * 30 + self.minute["time"] * 0.5)))
        self.minute["x"] = self.minute["length"] * math.cos(
            math.radians(90 - self.minute["time"] * 6))
        self.minute["y"] = self.minute["length"] * math.sin(
            math.radians(90 - self.minute["time"] * 6))
        self.second["x"] = self.second["length"] * math.cos(
            math.radians(90 - self.second["time"] * 6))
        self.second["y"] = self.second["length"] * math.sin(
            math.radians(90 - self.second["time"] * 6))

    def ConvertCoordinate(self): # 座標を変換
        self.hour["x"] = self.origin["x"] + self.hour["x"]
        self.hour["y"] = self.canvasHeight - (self.origin["y"] + self.hour["y"])
        self.minute["x"] = self.origin["x"] + self.minute["x"]
        self.minute["y"] = self.canvasHeight - (self.origin["y"] + self.minute["y"])
        self.second["x"] = self.origin["x"] + self.second["x"]
        self.second["y"] = self.canvasHeight - (self.origin["y"] + self.second["y"])

    def CreateWidgets(self):
        currentTime = datetime.datetime.now()
        self.label.destroy()
        self.canvas.delete("lines")
        self.canvas.create_line(
            self.origin["x"], self.origin["y"], self.hour["x"], self.hour["y"],
            fill="#ff0000", width=10, tag="lines")
        self.canvas.create_line(
            self.origin["x"], self.origin["y"], self.minute["x"], self.minute["y"],
            fill="#00ff00", width=5, tag="lines")
        self.canvas.create_line(
            self.origin["x"], self.origin["y"], self.second["x"], self.second["y"],
            fill="#0000ff", width=1, tag="lines")

        self.label = tk.Label(
            text=f"{currentTime.hour}時{currentTime.minute}分{currentTime.second}秒",
            font=("Times", 20))
        self.label.pack()

        self.after(100, self.ClockMain) # 100ms後にClockMain()を実行

    def ClockMain(self):
        self.getTime()
        self.CalcCoordinate()
        self.ConvertCoordinate()
        self.CreateWidgets()


try:  # ウインドウを高dpi環境に対応させる
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except: # 失敗した場合表示がおかしくなる
    pass

def main():
    clock = Clock(master=tk.Tk())
    clock.ClockMain()
    clock.bind("<Destroy>", lambda event: clock.destroy)
    clock.mainloop() # ↑ウインドウが破棄されたとき、メインループを抜ける

main()
