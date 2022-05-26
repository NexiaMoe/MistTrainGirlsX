# MistTrainGirlsX Private Server (WIP)

As the header speak, it still WIP and most of feature not work.

## What's working ?
- [x] Register (Through Nutaku as I can't change login logic)
- [x] Login
- [x] Daily login
- [x] Scene
- [ ] Item Storage System
- [ ] Character Storage System
- [ ] Mission 
- [ ] Gacha System
- [ ] Story

## How to run ?
1. You need :
    - Secondary browser (Firefox is recommended)
    - Charles Proxy (I use this), Fiddler, MITM Proxy, etc
    - Nutaku account
2. Set your Browser to use Proxy as mention above.
3. Install proxy certificate to browser or OS Level.
4. Create Self-signed SSL Cert, google it!
5. Open terminal, run

    ```uvicorn.exe run:app --ssl-keyfile private.key --ssl-certfile certificate.crt --reload --port 443``` 
6. On Proxy Software, Enable map remote (in Charles)

    - https://fd-mistglobal-prod-ntk.azurefd.net/Content/Js?v=2&adult=True  -->	https://127.0.0.1/Content/Js?v=2&adult=True
    - https://cdn2-mistglobal-prod-ntk.azureedge.net/prod-client-web-ntk/src/project.js -->	https://127.0.0.1/prod-client-web-ntk/src/project.js
7. Open the game. Enjoy
## Contributing

Contributions are always welcome!

### How to contributing ?
1. You need :
    - Secondary browser (Firefox is recommended)
    - Charles Proxy (I use this), Fiddler, MITM Proxy, etc
    - Nutaku account
2. Set your Browser to use Proxy as mention above.
3. Install certificate from proxy software to decrypt ssl.
4. Capture feature that you want to add.
5. Code to run.py


## Feedback

If you have any feedback, please reach out to us at [Discord](https://discord.com/invite/WmMPnNZYpG)

## License

[unlicense](https://github.com/NexiaMoe/MistTrainGirlsX/blob/master/LICENSE.md)

