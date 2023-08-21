Baseado no log abaixo, resolvi mudar a logica de teste de proxy:

Proxy:  20.44.206.138:80

<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">20.212.130.156</pre></body></html>

Proxy is not working.

Ou Seja, o proxy não é o IP publico retornado. Mas se o site é carregado e um IP é mostrado, então significa sucesso.

Então se não tiver exception, sinal de sucesso.

Para executar a partir da raiz do projeto:
docker build -t test_proxy_utils -f test_proxy_utils.Dockerfile . && docker run -d --name test_proxy_utils_container test_proxy_utils 