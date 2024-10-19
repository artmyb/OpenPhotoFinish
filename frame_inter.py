




















interpolation_factor = self.interpolation_factor
                    #self.frames_to_interpolate = [cv2.resize]
                    interpolated_frames = []

                    background_frame = self.framess[-1]

                    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST)

                    for i in range(len(self.framess) - 1):
                        frame1 = self.framess[i]
                        frame2 = self.framess[i + 1]

                        flow = dis.calc(frame1, frame2, None)
                        #flow[..., 1] = 0
                        interpolated_frames.append(frame1)

                        for j in range(1, interpolation_factor):
                            if self.abort:
                                polygon_points = [self.status.winfo_width() - 600, 5,
                                                  self.status.winfo_width() - 600,
                                                  5, self.status.winfo_width() - 600,
                                                  self.status.winfo_height() - 5,
                                                  self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                                self.status.coords(self.progress_bar, polygon_points)
                                self.status.itemconfig(self.status_text, text=" ", font=self.font)
                                self.image_in_progress = False
                                self.abort = False
                                return
                            alpha = j / interpolation_factor
                            flow_scaled = flow * alpha

                            h, w = flow.shape[:2]
                            flow_map_x, flow_map_y = np.meshgrid(np.arange(w), np.arange(h))
                            flow_map_x = (flow_map_x - flow_scaled[..., 0]).astype(np.float32)
                            flow_map_y = (flow_map_y - flow_scaled[..., 1]).astype(np.float32)
                            flow_map = np.stack((flow_map_x, flow_map_y), axis=-1)

                            intermediate_frame = cv2.remap(frame1, flow_map, None, cv2.INTER_LINEAR)

                            static_mask = np.abs(background_frame - intermediate_frame) < 5

                            intermediate_frame_corrected = np.where(static_mask, background_frame, intermediate_frame)

                            interpolated_frames.append(intermediate_frame_corrected)

                        polygon_points = [self.status.winfo_width() - 600, 5,
                                              self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              5, self.status.winfo_width() - 600 + int(((i + 1) / len(self.framess)) * 600),
                                              self.status.winfo_height() - 5,
                                              self.status.winfo_width() - 600, self.status.winfo_height() - 5]

                        self.status.coords(self.progress_bar, polygon_points)
                        self.status.itemconfig(self.status_text, text="Interpolating frames: " + str(
                            int(100 * (i + 1) / len(self.framess))) + " %", font=self.font)


                    interpolated_frames.append(self.framess[-1])