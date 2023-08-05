# Conduits - A Declarative Pipelining Tool For Pandas
Traditional tools for declaring pipelines in Python suck. They are mostly 
imperative, and can sometimes requires that you adhere to strong contracts in
order to use them (looking at you Scikit Learn pipelines ��). It is also 
usually done completely differently to the way the pipelines where developed 
during the ideation phase, requiring significate rewrite to get them to work
in the new paradigm.

Modelled off the declarative pipeline of Flask, **Tether** aims to give you a
nicer, simpler, and more flexible way of declaring your data processing pipelines.

## Installation

```bash
pip install conduits
```