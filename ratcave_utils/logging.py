import csv
import ratcave as rc
import motive
import time
from os import path
import warnings

class Logger(rc.utils.Observer):

    columns=('MotiveTime', 'Time',
             'Class', 'Name', 'Visible',
             'x', 'y', 'z',
             'rot_x', 'rot_y', 'rot_z',
             'quat_w', 'quat_x', 'quat_y', 'quat_z',
             'glob_x', 'glob_y', 'glob_z',
             'ori_x', 'ori_y', 'ori_z',
             'glob_ori_x', 'glob_ori_y', 'glob_ori_z',
             )

    def __init__(self, fname, overwrite=False, **kwargs):
        """Creates a CSV Logging object that writes whenever registered ratcave Observable objects change."""
        super(Logger, self).__init__(**kwargs)
        if path.exists(fname):
            if overwrite:
                warnings.warn('Overwriting existing logfile {}'.format(fname))
            else:
                raise IOError("LogFile {} already exists.".format(fname))
        self.fname = fname
        self.writer = None
        self.f = None

    def open(self):
        self.f = open(self.fname, 'wb')
        self.writer = csv.DictWriter(self.f, fieldnames=self.columns)
        self.writer.writeheader()

    def close(self):
        self.f.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def on_change(self):
        super(Logger, self).on_change()

        if self._changed_observables:
            motive_tt = motive.frame_time_stamp()
            tt = time.clock()
            for obs in self._changed_observables:
                line = {}
                line['MotiveTime'] = motive_tt
                line['Time'] = tt
                line['Name'] = obs.name
                line['Class'] = obs.__class__.__name__
                line['Visible'] = obs.visible
                line['x'], line['y'], line['z'] = obs.position.xyz
                rot_euler = obs.rotation.to_euler(units='rad')
                line['rot_x'], line['rot_y'], line['rot_z'] = rot_euler.xyz
                rot_quat = obs.rotation.to_quaternion()
                line['quat_w'], line['quat_x'], line['quat_y'], line['quat_z'] = rot_quat.wxyz
                line['glob_x'], line['glob_y'], line['glob_z'] = obs.position_global
                line['ori_x'], line['ori_y'], line['ori_z'] = obs.orientation
                line['glob_ori_x'], line['glob_ori_y'], line['glob_ori_z'] = obs.orientation_global
                self.writer.writerow(line)


    def add_observables(self, *observables):
        """Convenience function for logging, which simply calls the register_observer(log) method on each observable."""
        for observable in observables:
            observable.register_observer(self)