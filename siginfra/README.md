# SIG-Infra
O SIG-Infra foi desenvolvido como uma solução para a gestão de infraestrutura de campi universitários. Com ele, é possível cadastrar informações sobre ambientes (salas de aula, escritórios, auditórios, etc), também sobre os edifícios onde esses ambientes estão localizados e os respectivos campi onde se encontram esses edifícios.

# Dependências

A aplicação SIG-Infra foi desenvolvida usando o framework [Flask](https://flask.palletsprojects.com/en/1.1.x/) para Python. Algumas extensões para o Flask também são utilizadas:

- [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [flask_bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [flask_login](https://flask-login.readthedocs.io/en/latest/)
- [flask_wtf](https://flask-wtf.readthedocs.io/en/stable/)

Além do Flask e suas extensões, também é necessário importar as seguintes bibliotecas:

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [wtforms](https://wtforms.readthedocs.io/en/2.3.x/) e sua extensão para o SQLAlchemy, [wtforms_sqlalchemy](https://pypi.org/project/WTForms-SQLAlchemy/)

