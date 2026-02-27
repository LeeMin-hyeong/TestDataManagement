from pyloid_builder.pyinstaller import pyinstaller
from pyloid_builder.optimize import optimize
from pyloid.utils import get_platform
from pathlib import Path


main_script = './src-pyloid/main.py'
name = 'main'
updater_script = './src-pyloid/updater.py'
entry_name = 'tdm'
dist_path = './dist'
work_path = './build'


if get_platform() == 'windows':
	icon = './src-pyloid/icons/tdm_icon.ico'
elif get_platform() == 'macos':
	icon = './src-pyloid/icons/tdm_icon.png'
else:
	icon = './src-pyloid/icons/tdm_icon.png'

if get_platform() == 'windows':
    optimize_spec = './src-pyloid/build/windows_optimize.spec'
elif get_platform() == 'macos':
    optimize_spec = './src-pyloid/build/macos_optimize.spec'
else:
    optimize_spec = './src-pyloid/build/linux_optimize.spec'



if __name__ == '__main__':
	main_add_data = [
		'--add-data=./src-pyloid/icons/:./src-pyloid/icons/',
		'--add-data=./dist-front/:./dist-front/',
		'--add-data=./LICENSE:./',
	]
	if Path('./license.json').exists():
		main_add_data.append('--add-data=./license.json:./')

	pyinstaller(
		main_script,
		[
			f'--name={name}',
			f'--distpath={dist_path}',
			f'--workpath={work_path}',
			'--clean',
			'--noconfirm',
			'--onedir',
			# '--onefile',
			'--windowed',
			'--hidden-import=selenium.webdriver.chrome.webdriver',
			*main_add_data,
			f'--icon={icon}',
		],
	)
	pyinstaller(
		updater_script,
		[
			f'--name={entry_name}',
			f'--distpath={dist_path}',
			f'--workpath={work_path}',
			'--clean',
			'--noconfirm',
			'--onefile',
			'--windowed',
			'--add-data=./src-pyloid/icons/:./src-pyloid/icons/',
			'--add-data=./src/assets/tdm.png:./src/assets',
			f'--icon={icon}',
		]
	)

	if get_platform() == 'windows':
		optimize(f'{dist_path}/{name}/_internal', optimize_spec)
	elif get_platform() == 'macos':
		optimize(f'{dist_path}/{name}.app', optimize_spec)
	else:
		optimize(f'{dist_path}/{name}/_internal', optimize_spec)
