from setuptools import setup, find_packages

setup(
    name='ratcave_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=['click', 'numpy', 'pyglet'],  # TODO: Find out how to list OpenCV-2 (cv2 didn't work)
    entry_points={
        'console_scripts': [
            'ratcave_utils = ratcave_utils:cli',
            'calib_projector = ratcave_utils.calib_projector:calib_projector',
            'trackrotation = ratcave_utils.track_rigidbody:trackrotation',
            'trackposition = ratcave_utils.track_rigidbody:trackposition',
            'scan_arena = ratcave_utils.arena_scanner:scan_arena',
            'dots_test = ratcave_utils.dots_test:show_dots',
            'view_mesh = ratcave_utils.view_mesh:view_mesh',
            'view_arenafit = ratcave_utils.view_arenafit:view_arenafit',
            'vr_demo = ratcave_utils.vr_demo:vr_demo',
            'latency_test = ratcave_utils.latency_test:latency_test'
        ],
    }
)
