import cv2
import numpy as np
import progressbar

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
        self.writer = cv2.VideoWriter(self.videofname, cv2.VideoWriter_fourcc(*'XVID'), 25.0, (self.window_x_size, self.window_y_size), True)

    def start_window(self):
        self.current_window = np.ones((self.window_y_size, self.window_x_size, 3), dtype=np.uint8)
        self.current_window[:, :] = 255
        cv2.rectangle(self.current_window,
                      (self.margin, self.margin),
                      (self.virtxsize + self.margin, self.virtysize + self.margin),
                      (255, 0, 0), 2)
        #self.windows.append(window)

    def get_current_window(self):
        return self.windows[-1] if len(self.windows) > 0 else None

    def get_circle_ji(self, x, y):
        j = int(x*self.multj) - 1 + self.margin
        i = self.window_y_size - (int(y*self.multi) -1) - self.margin
        return j, i

    def add_circle(self, x, y, rad1, rad2, c=(0,0,255)):
        j = int(x*self.multj) - 1 + self.margin
        i = self.window_y_size - (int(y*self.multi) -1) - self.margin
        #print("adding circle %d %d" %(j,i))
        cv2.circle(self.current_window, (j, i), rad1, c, rad2)

    def add_frame(self):
        self.writer.write(self.current_window)


    def create_video(self):
        #for window in self.windows:
        #    writer.write(window)
        self.writer.release()
        cv2.destroyAllWindows()

    @staticmethod
    def generate_video(results, videofname, window_x_size, window_y_size, real_width, real_height, margin=50, rc=2):
        visual_radius = 2
        video_tool = VideoTool(videofname, window_x_size, window_y_size,real_width, real_height, margin=margin)
        rbor = int(rc * min(video_tool.multj, video_tool.multi))
        with progressbar.ProgressBar(max_value=len(results)) as bar:
            for n, result in enumerate(results):
                video_tool.start_window()
                for x, y in result:
                    video_tool.add_circle(x, y, visual_radius, visual_radius * 2)
                    video_tool.add_circle(x, y, rbor, 0, c=(0, 255, 0, 100))

                video_tool.add_frame()
                bar.update(n)
        video_tool.create_video()