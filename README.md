# Processamento de Imagens e Visão Computacional

Este repositório reúne pequenas bibliotecas, programas, funções e implementações de algoritmos simples ou não tão simples para Processamento de Imagens e Visão Computacional. A maior parte dos códigos encontrados aqui são resultado da preparação de aulas, trabalhos e provas para disciplinas como *Processamento Digital de Sinais*, *Processamento de Imagens*, *Computação Gráfica* e outras relacionadas.

Não há a intenção de criar algoritmos eficientes ou módulos a serem usados em produção: o principal objetivo é que os códigos gerados sejam legíveis e fáceis de serem compreendidos. Assim, não se deve esperar que os programas aqui sejam incrivelmente eficientes, e nem que exista uma organização perfeita da distribuição e utilização dos programas fonte. Também não há dedicação a uma linguagem de programação específica, embora várias delas tenham bastante conteúdo vindo da prática diária.

Ainda assim, vários dos programas -- especialmente as mini-bibliotecas -- podem ser usadas para duas aplicações básicas. A primeira dela é como ferramenta para a educação e o aprendizado. As bibliotecas foram criadas de tal forma que seu código possa ser estudado e compreendido de maneira simples, as imagens são tratadas apenas em um único tipo de dado (`float` ou `double`), de tal maneira que não exista a preocupação com *overflow* e *underflow* (que causam efeitos desagradáveis à vista no resultado final).

A segunda aplicação é a *prototipagem* de aplicações mais densas. Devido à facilidade de uso, o programador pode se concentrar em obter resultados que, posteriormente, podem ser convertidos para linguagens ou bibliotecas cujo foco seja a eficiência.

Segue abaixo uma lista das implementações interessantes:

* Algoritmos:
  * *Romerizator*: um pequeno *script* para a geração de pinturas bregas a partir de fotos. O programa é disponibilizado de duas formas diferentes: na forma de um *notebook* do Jupyter contendo comentários e explicações mais detalhadas sobre seu funcionamento, e que faz a conversão de uma única imagem; e um *script* que pode ser rodado na linha de comando, e que processa todas as imagens em formato `.png` disponíveis em um diretório.

Em breve, mais programas serão incluídos aqui.
