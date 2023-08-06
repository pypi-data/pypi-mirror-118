# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genetic_algorithms', 'genetic_algorithms.examples', 'genetic_algorithms.test']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'genetic-algorithms',
    'version': '1.0.1',
    'description': 'This library is a wrapper for genetic algorithms to leverage in optimisation problems.',
    'long_description': '# Genetic Algorithms for python\n[![Build Status](https://travis-ci.org/GitToby/genetic_algorithms.svg?branch=master)](https://travis-ci.org/GitToby/genetic_algorithms)\n\nThis library is a wrapper for genetic algorithms to leverage in optimisation problems.\nIt hopes to make writing infinitely customizable genetic algorithms easy and quick while having all the standard features expected.\n\n# Installation\nThis module can be installed via pip:\n```bash\npip install genetic-algorithms\n```\n\n# Roadmap\n* add mutation potency & frequency, extract population flow to user defined sequence.\n* add multi population models\n* add common crossover and mutation generic methods\n\n# Examples\nThis is a basic example for maximising values in a list, starting with 10 members running 100 generation.\nThen it will log to the screen and create a csv file with each generations information in short format.\n\n```python\nimport genetic_algorithms as ga\nimport random\n\nclass MyMember(ga.MemberBase):\n    def _construct_from_params(self, construction_parameters=None):\n        # Starting point is a bunch of 5 numbers [0-9]\n        self.vars = [random.randrange(10) for _ in range(5)]\n\n    def mutate(self):\n        # Mutation involves adding a number between -2 and 2 to a random variable\n        i = random.randrange(-2,3)\n        j = random.randrange(len(self.vars))\n        self.vars[j] += i\n\n    def crossover(self, pairing):\n        # Crossing over takes the first half from member one, and the second half from member 2\n        new_params = self.vars[:len(self.vars) // 2] + pairing.vars[len(pairing.vars) // 2:]\n        return MyMember(new_params)\n\n    def score_self(self):\n        return sum(self.vars)\n\ndef m_fit_func(member: MyMember):\n    # This scores the member on its properties, but can involve any external functions as needed.\n    # Remember to test this does what you want.\n    return member.score_self()\n\npop = ga.Population(size=10, member_type=MyMember, member_parameters_generator=None,\n                   fitness_function=m_fit_func, population_seed=0)\npop.run(100, print_logging=True, csv_path="example1.csv")\n```\n\nThis next one is a little more complected; we want to identify a door of a particular size.\n```python\nimport genetic_algorithms as ga\nimport random\nimport numpy as np\n\n\nclass Door(ga.MemberBase):\n    def _construct_from_params(self, construction_parameters=None):\n        # Set the parameters as passed by the generator\n        self.height = construction_parameters[\'height\']\n        self.width = construction_parameters[\'width\']\n\n    def mutate(self):\n        # Mutate by adding 1 or -1 to our door height and width.\n        # this is an example of a bad mutation function because it wouldn\'t hit an integer after the mutation\n        i = random.randrange(2)\n        j = random.randrange(2)\n        self.height += pow(-1, i)\n        self.width += pow(-1, j)\n\n    def crossover(self, pairing):\n        # Again a bad example of a crossover, the mean we will converge quickly but very hard to get a precice score.\n        new_params = {\'height\': np.mean([self.height, pairing.height]),\n                      \'width\': np.mean([self.width, pairing.width])}\n        return Door(construction_parameters=new_params)\n\n    def __repr__(self):\n        return \'height: \' + str(self.height) + " | width: " + str(self.width)\n\n\ndef fit_through_door(member: Door):\n    door_height = 10\n    door_width = 3\n    height_diff = abs(door_height - member.height)\n    width_diff = abs(door_width - member.width)\n    return height_diff + width_diff\n\ndef param_generator():\n    max_h = 10\n    max_w = 20\n    yield {\'height\': random.randrange(max_h),\n           \'width\': random.randrange(max_w)}\n\nrandom.seed(1)\npop = ga.Population(100, Door, fit_through_door, member_parameters_generator=param_generator)\n# run 500 generations before checking we have some parameters changed\npop.run(generations=500, print_logging=True, maximise_fitness_func=False)\nprint("Best door:", pop.get_top())\n# returns what almost exactly what we want:\n# Best door: (height: 9.999995902180672 | width: 3.999865485355258, 244033.23286180547)\n```\n\nFinally, we will boost it to a very complicated example, we want to generate a copy of a picture of a face from a randomly generated face.\n',
    'author': 'Toby',
    'author_email': 'toby@thedevlins.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GitToby/genetic_algorithms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
