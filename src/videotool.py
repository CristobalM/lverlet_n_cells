import cv2
import numpy as np


class VideoTool:
    def __init__(self, videofname, window_x_size, window_y_size, real_width, real_height, margin=50):
        self.videofname = videofname
        self.window_x_size = window_x_size
        self.window_y_size = window_y_size
        self.real_width = real_width
        self.real_height = real_height
        self.margin = int(margin)
        self.current_window_index = 0
        self.current_window = None
        self.windows = []
        self.virtxsize = int(window_x_size - 2 * margin)
        self.virtysize = int(window_y_size - 2 * margin)
        self.multj = self.virtxsize / real_width
        self.multi = self.virtysize / real_height
        print("window_x_size=%d"%window_x_size)
        print("window_y_size=%d"%window_y_size)
        print("real_width=%d"%real_width)
        print("real_height=%d"%real_height)
        print("margin=%d"%margin)

    def start_window(self):
        window = np.ones((self.window_y_size, self.window_x_size, 3), dtype=np.uint8)
        window[:, :] = 255
        cv2.rectangle(window,
                      (self.margin, self.margin),
                      (self.virtxsize + self.margin, self.virtysize + self.margin),
                      (255, 0, 0), 2)
        self.windows.append(window)

    def get_current_window(self):
        return self.windows[-1] if len(self.windows) > 0 else None

    def get_circle_ji(self, x, y):
        j = int(x*self.multj) - 1 + self.margin
        i = self.window_y_size - (int(y*self.multi) -1) - self.margin
        return j, i

    def add_circle(self, x, y, rad1, rad2, c=(0,0,255)):
        window = self.get_current_window()
        j = int(x*self.multj) - 1 + self.margin
        i = self.window_y_size - (int(y*self.multi) -1) - self.margin
        #print("adding circle %d %d" %(j,i))
        cv2.circle(window, (j, i), rad1, c, rad2)

    def create_video(self):
        writer = cv2.VideoWriter(self.videofname, cv2.VideoWriter_fourcc(*'XVID'), 25.0, (self.window_x_size, self.window_y_size), True)

        for window in self.windows:
            writer.write(window)
        writer.release()
        cv2.destroyAllWindows()