.PHONY: test run demo figures

test:
	python -m unittest discover -s tests -v

run:
	python run_pipeline.py --input data/raw/ml_alfabetizacao.csv

demo:
	python run_pipeline.py --input tests/fixtures/amostra_teste_sintetica.csv --demo

figures:
	python scripts/generate_static_figures.py
