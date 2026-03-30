async function test() {
  const res = await fetch("https://openapi-gateway-azero.soundai.com/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Accept": "text/event-stream",
      "Content-Type": "application/json",
      "Authorization": "Bearer CqTMsc0z5pdcr4hiDtsD/84VzuaxaqHCDtSxFXyzNvwyuIkoRTHNeR5dGW3XGmqf0SejOjhZpcya3mT6G1eXEA=="
    },
    body: JSON.stringify({
      model: "soundai/azerogpt",
      messages: [{role: "user", content: "你好"}],
      max_tokens: 10,
      stream: true
    })
  });
  console.log("Bearer Status:", res.status);
  const text = await res.text();
  console.log("Response:", text.slice(0, 100));
}
test();
