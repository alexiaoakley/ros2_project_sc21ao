from setuptools import find_packages, setup

package_name = 'ros2_project_sc21ao'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cscajb',
    maintainer_email='x.wang16@leeds.ac.uk',
    description='ROS2 Project for RGB Detection and Motion Planning',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'first_step = ros2_project_sc21ao.first_step:main',
            'second_step = ros2_project_sc21ao.second_step:main',
            'third_step = ros2_project_sc21ao.third_step:main',
            'fourth_step = ros2_project_sc21ao.fourth_step:main',
            'robot_task = ros2_project_sc21ao.robot_task:main',  # Registering robot_task.py here
        ],
    },
)
