from setuptools import find_packages, setup

package_name = 'crazyflie_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         ('share/' + package_name + '/launch', ['launch/swarm_mapping.launch.py'])
        #  ('share/' + package_name + '/launch', ['launch/default_map.launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yanyew',
    maintainer_email='lowyanyew@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
