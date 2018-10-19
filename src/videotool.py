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

    def get_current_window(self):
        return self.windows[-1] if len(self.windows) > 0 else None

    def get_circle_ji(self, x, y):
        j = int(x*self.multj) - 1 + self.margin
        i = self.window_y_size - (int(y*self.multi) -1) - self.margin
        return j, i

    def get_drawing_radius(self, real_radius):
        return int(real_radius * max(self.multj, self.multi))

    def add_circle(self, x, y, rad, c=(0,0,255), thickness=1):
        j, i = self.get_circle_ji(x, y)
        vrad = self.get_drawing_radius(rad)
        cv2.circle(self.current_window, (j, i), vrad, c, thickness=thickness)

    def get_point_in_direction(self, j, i, angle, rad):
        vrad = self.get_drawing_radius(rad)
        j_out = int(j + vrad*np.cos(angle))
        i_out = int(i - vrad*np.sin(angle))
        return j_out, i_out

    def add_line(self, x1, y1, x2, y2, c=(0, 255, 255)):
        j1, i1 = self.get_circle_ji(x1, y1)
        j2, i2 = self.get_circle_ji(x2, y2)
        cv2.line(self.current_window, (j1, i1), (j2, i2), color=c)

    def add_line_warrow(self, x1, y1, angle, angle_arrow, radius, c=(0, 0, 255)):
        j1, i1 = self.get_circle_ji(x1, y1)
        j2, i2 = self.get_point_in_direction(j1, i1, angle, radius)

        cv2.line(self.current_window, (j1, i1), (j2, i2), color=c, thickness=2)

        deltay = -(i2 - i1)
        deltax = j2 - j1

        r = np.sqrt(deltax**2 + deltay**2)
        phi = np.arctan2(deltay, deltax)
        alpha = angle_arrow + phi + np.pi/2
        beta = -angle_arrow + phi - np.pi/2

        r2 = r/4

        ja1 = int(j2 + r2*np.cos(alpha))
        ia1 = int(i2 - r2*np.sin(alpha))

        ja2 = int(j2 + r2*np.cos(beta))
        ia2 = int(i2 - r2*np.sin(beta))

        arrow_triangle = np.array([[j2, i2], [ja1, ia1], [ja2, ia2]], np.int32)
        arrow_triangle = arrow_triangle.reshape((-1, 1, 2))

        cv2.fillPoly(self.current_window, [arrow_triangle], color=c)

    def add_text_between(self, x1, y1, x2, y2, text):
        j1, i1 = self.get_circle_ji(x1, y1)
        j2, i2 = self.get_circle_ji(x2, y2)

        mi = int((i1+i2)/2)
        mj = int((j1+j2)/2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (mj, mi)
        fontScale = 0.5
        fontColor = (0, 0, 0)
        lineType = 2

        cv2.putText(self.current_window, text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

    def add_text(self, x, y, text):
        j, i = self.get_circle_ji(x, y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (j, i)
        fontScale = 0.5
        fontColor = (200, 200, 200)
        lineType = 2

        cv2.putText(self.current_window, text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

    def add_frame(self):
        self.writer.write(self.current_window)

    def create_video(self):
        self.writer.release()
        cv2.destroyAllWindows()

    @staticmethod
    def generate_video(results, videofname, window_x_size, window_y_size, real_width, real_height, margin=50, rc=2,
                       all_sim_angles=None, all_interactions_list=None):
        video_tool = VideoTool(videofname, window_x_size, window_y_size,real_width, real_height, margin=margin)
        final_radius = rc/2.0
        with progressbar.ProgressBar(max_value=len(results)) as bar:
            for n, result in enumerate(results):
                video_tool.start_window()
                for k_particle, (x, y) in enumerate(result):
                    video_tool.add_circle(x, y, rc/10, thickness=-1)
                    video_tool.add_circle(x, y, final_radius, c=(0, 255, 0, 100))
                    video_tool.add_text(x, y, str(k_particle))

                    if all_sim_angles is not None:
                        angle = all_sim_angles[n][k_particle]
                        video_tool.add_line_warrow(x, y, angle, np.pi/4, final_radius, c=(255, 0, 0))

                    if all_interactions_list is not None:
                        for other_idx, [forcex, forcey] in all_interactions_list[n][k_particle]:
                            [other_x, other_y] = result[other_idx]
                            force = np.round(np.sqrt(forcex**2 + forcey**2), 3)
                            color = (0, 255, 255) if force <= 0.0 else (255, 0, 255)
                            video_tool.add_line(x, y, other_x, other_y, c=color)
                            video_tool.add_text_between(x, y, other_x, other_y, str(force))

                video_tool.add_frame()
                bar.update(n)
        video_tool.create_video()