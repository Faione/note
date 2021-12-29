export JAEGER_AGENT_HOST=127.0.0.1
export JAEGER_AGENT_PORT=6831
export JAEGER_SAMPLING_ENDPOING=http://127.0.0.1:5778/sampling

./hotrod all

hotrod-container:v0.1