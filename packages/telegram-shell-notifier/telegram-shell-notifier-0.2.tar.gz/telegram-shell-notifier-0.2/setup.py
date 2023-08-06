from setuptools import setup
from os.path import join, dirname

setup(
      name='telegram-shell-notifier',
      version='0.2',
      description='Simple telegram notifier, ready for shell usage',
      url='http://github.com/airens/telegram_notifier',
      author='Valeriy Chistyakov',
      author_email='airens@mail.ru',
      license='MIT',
      packages=['telegram_shell_notifier'],
      install_requires=['requests', 'argparse'],
      zip_safe=False,
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      long_description_content_type="text/markdown"
)
