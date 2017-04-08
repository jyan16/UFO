import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-year', required = True, default = '2017')
	opts = parser.parse_args()
	print('what the fuck')


if __name__ == '__main__':
	main()