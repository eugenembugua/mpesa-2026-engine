from setuptools import setup

setup(
    name="mpesa_prototype_2026",
    version="1.0.0",
    author="Eugene Mbugua",
    description="A high-fidelity M-Pesa engine",
    #Tells setup.py to look for individual .py files in the current directory
<<<<<<< HEAD
    py_modules=["main", "engine", "models", "security", "data_logger", "dashboard", "sync_rates", "statement_service"],
    install_requires=[
        'pandas', #For dashboarding and CSV handling
        'stdiomask',
        'requests',
        'fpdf2'
=======
    py_modules=["main", "engine", "models", "security", "data_logger", "dashboard"],
    install_requires=[
        'pandas', #For dashboarding and CSV handling
        'stdiomask'
>>>>>>> 90f26134e12423dae4455a9bd4164f27843b7d4c
    ],
    python_requires='>=3.13',
    entry_points={
        'console_scripts': [
            'mpesa-app=main:main', #Allows user to run the app by typing 'mpesa-app' in terminal
        ],
    },
)