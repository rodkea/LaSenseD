from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget
from queue import Queue
import os
import time

class RecordThread(QThread):

  MEASURED_FPS_FORMAT = "{:06.2f}"
  FRAME_COUNT_DIGITS = 4

  def __init__(self, filename: str, resolution: tuple[int, int], queue : Queue, parent: QWidget | None = None):
    super().__init__(parent)
    self._queue = queue
    self._filename = self._generate_unique_filename(filename)
    self._resolution = resolution
    self._frame_counter = 0
    self._measured_fps_value = 0.0

  def _generate_unique_filename(self, filename: str) -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    filepath = os.path.join(root_dir, f"data/videos/{filename}.ls")
    if not os.path.exists(filepath): # Si no existe, retornamos directamente
      return filepath    
    counter = 1     # Si existe, probamos con sufijos (1), (2), ...
    while True:         
      new_filepath =  os.path.join(root_dir, f"data/videos/{filename}({counter}).ls")
      if not os.path.exists(new_filepath):
        return new_filepath
      counter += 1


  def run(self):
     self._frame_counter = 0
     self._measured_fps_value = 0.0
     start_time = None
     with open(self._filename, 'wb') as f:      

      measured_fps_placeholder_str = self.MEASURED_FPS_FORMAT.format(0.0) # Initial placeholder like "000.00"
      frame_count_placeholder_str = '0' * self.FRAME_COUNT_DIGITS
      header_part1_str = f"Version:1.0, Resolution: {self._resolution}, MeasuredFPS: "
        #  will be inserted here
      header_part2_str = f", NumberOfFrames: "
      header_part3_newline_str = "\n"
      initial_header_str = (header_part1_str +
        measured_fps_placeholder_str +
        header_part2_str +
        frame_count_placeholder_str +
        header_part3_newline_str
      )
      initial_header_bytes = initial_header_str.encode('utf-8')
      
      # --- Calculate byte offsets for overwriting placeholder VALUES ---
        # Offset for the start of the MeasuredFPS numeric value
      measured_fps_value_offset = len(header_part1_str.encode('utf-8'))
        # Offset for the start of the NumberOfFrames numeric value
      frame_count_value_offset = (
        len(header_part1_str.encode('utf-8')) +
        len(measured_fps_placeholder_str.encode('utf-8')) + # Length of the FPS placeholder string
        len(header_part2_str.encode('utf-8'))
      )
      f.write(initial_header_bytes)
      start_time = time.monotonic()
      while not self.isInterruptionRequested():
        if not self._queue.empty():          
          self._queue.get().tofile(f)
          self._frame_counter += 1
      end_time = time.monotonic() # Record end time after loop

      # --- Calculate Measured FPS ---
      calculated_fps = 0.0
      if self._frame_counter > 0 and start_time is not None:
          duration_seconds = end_time - start_time
          if duration_seconds > 0:
              calculated_fps = self._frame_counter / duration_seconds
          elif self._frame_counter > 0: # Duration is ~0 but frames exist
              print("Warning: Recording duration too short for accurate FPS; may appear as 0.00 or very high if not capped.")
              # calculated_fps will be 0.0 or very high if not capped below.
              # For now, if duration is 0, we'll let it be 0.0 or a capped high value.
      
      self._measured_fps_value = calculated_fps # Store for potential display

      # Format Measured FPS string for header, capping to fit placeholder (e.g., max 999.99)
      # Ensure the formatted string exactly matches the placeholder length.
      actual_measured_fps_str = self.MEASURED_FPS_FORMAT.format(min(calculated_fps, 999.99))
      actual_measured_fps_bytes = actual_measured_fps_str.encode('utf-8')

      # --- Format NumberOfFrames string for header (same logic as before) ---
      max_frames_for_placeholder = (10**self.FRAME_COUNT_DIGITS) - 1
      final_frame_count_to_write = min(self._frame_counter, max_frames_for_placeholder)
      if self._frame_counter > max_frames_for_placeholder:
          print(f"Warning: Frame count ({self._frame_counter}) exceeded placeholder. Storing capped value.")
      actual_frame_count_digits_str = "{:0{width}d}".format(final_frame_count_to_write, width=self.FRAME_COUNT_DIGITS)
      actual_frame_count_digits_bytes = actual_frame_count_digits_str.encode('utf-8')
      
      # --- Update placeholders in the file ---
      # Update Measured FPS
      f.seek(measured_fps_value_offset)
      f.write(actual_measured_fps_bytes)
      
      # Update NumberOfFrames
      f.seek(frame_count_value_offset)
      f.write(actual_frame_count_digits_bytes)      
  
  def stop(self):
    print("Vaciando buffer....")
    while not self._queue.empty():
      try:
        self._queue.get_nowait()
      except:
        break
    print("Buffer vacio")
    self.requestInterruption()
    self.wait()