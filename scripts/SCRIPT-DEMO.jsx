 // Função para processar as imagens com diferentes tamanhos de fonte e cores
 function processarImagensComDiferentesConfiguracoes() {
    // Pedir ao usuário para selecionar a pasta
    var pastaOrigem = Folder.selectDialog("Selecione a pasta com as fotos");

    // Verificar se o usuário cancelou a seleção da pasta
    if (!pastaOrigem) {
        alert("Nenhuma pasta selecionada. Processo cancelado.");
        return;
    }

    // Obtém a lista de arquivos na pasta de origem
    var arquivos = pastaOrigem.getFiles("*.*"); // Todos os arquivos na pasta

    for (var i = 0; i < arquivos.length; i++) {
        // Verifica se o arquivo é uma imagem (assumindo que todos são JPG)
        if (arquivos[i] instanceof File && arquivos[i].name.match(/\.(jpg|jpeg|png|gif|bmp|tif|tiff)$/i)) {
            // Abre a imagem
            var imagem = app.open(arquivos[i]);

            // Obtém as dimensões da imagem
            var largura = imagem.width;
            var altura = imagem.height;

            // Determinar o tamanho da fonte e a cor com base nas dimensões da imagem
            var tamanhoFonte, corRGB;
            if ((largura === 4838 && altura === 3456) || 
            (largura === 2469 && altura === 3456) ||
            (largura === 2345 && altura === 3283) ||
            (largura === 2857 && altura === 4000) ||
            (largura === 2637 && altura === 3692) ||
            (largura === 5182 && altura === 3701) ||
            (largura === 2741 && altura === 3838) ||
            (largura === 2716 && altura === 3803) ||
            (largura === 5600 && altura === 4000) ||
            (largura === 2612 && altura === 3657) ||
            (largura === 2632 && altura === 3685) ||
            (largura === 4675 && altura === 3339) ||
            (largura === 2607 && altura === 3650) ||
            (largura === 2381 && altura === 3334) ||
            (largura === 5446 && altura === 3890) ||
            (largura === 4516 && altura === 3226) ||
            (largura === 2648 && altura === 3707) ||
            (largura === 2656 && altura === 3718) ||
            (largura === 2751 && altura === 3851) ||
            (largura === 5209 && altura === 3721) ||
            (largura === 5152 && altura === 3680) ||
            (largura === 2739 && altura === 3835) ||
            (largura === 5149 && altura === 3678) ||
            (largura === 2728 && altura === 3819) ||
            (largura === 2546 && altura === 3564) ||
            (largura === 2724 && altura === 3814) ||
            (largura === 2649 && altura === 3709) ||
            (largura === 2569 && altura === 3597) ||
            (largura === 4454 && altura === 3181) ||
            (largura === 2239 && altura === 3274) ||
            (largura === 2277 && altura === 3188) ||
            (largura === 2280 && altura === 3192) ||
            (largura === 2684 && altura === 3757) ||
            (largura === 2561 && altura === 3586) ||
            (largura === 2616 && altura === 3662) ||
            (largura === 2357 && altura === 3300) ||
            (largura === 2191 && altura === 3286) ||
            (largura === 2621 && altura === 3670) ||

            (largura === 4528 && altura === 3234)) {
            tamanhoFonte = 10;
            corRGB = [255, 255, 255]; // BRANCA
        } else if ((largura === 2304 && altura === 3456) || 
                   (largura === 5184 && altura === 3456) ||
                   (largura === 2215 && altura === 3322) ||
                   (largura === 4838 && altura === 3225) ||
                   (largura === 2243 && altura === 3365) ||
                   (largura === 2339 && altura === 3509) ||
                   (largura === 2571 && altura === 3856) ||
                   (largura === 2248 && altura === 3372) ||
                   (largura === 2559 && altura === 3839) ||
                   (largura === 2633 && altura === 3950) ||
                   (largura === 2551 && altura === 3826) ||
                   (largura === 2501 && altura === 3751) ||
                   (largura === 2667 && altura === 4000) ||
                   (largura === 2505 && altura === 3758) ||
                   (largura === 6000 && altura === 4000) ||
                   (largura === 2559 && altura === 3939) ||
                   (largura === 2530 && altura === 3795) ||
                   (largura === 2419 && altura === 3629) ||
                   (largura === 2563 && altura === 3845) ||
                   (largura === 2561 && altura === 3842) ||
                   (largura === 2583 && altura === 3875) ||
                   (largura === 2550 && altura === 3825) ||
                   (largura === 2457 && altura === 3686) ||
                   (largura === 2542 && altura === 3813) ||
                   (largura === 6000 && altura === 4000) ||
                   (largura === 2539 && altura === 3808) ||
                   (largura === 2489 && altura === 3733) ||
                   (largura === 2598 && altura === 3897) ||
                   (largura === 2479 && altura === 3719) ||
                   (largura === 2539 && altura === 3809) ||
                   (largura === 2456 && altura === 3684) ||
                   (largura === 2565 && altura === 3848) ||
                   (largura === 2544 && altura === 3816) ||
                   (largura === 2559 && altura === 3939) ||
                   (largura === 2231 && altura === 3347)) {
            tamanhoFonte = 14;
            corRGB = [0, 0, 0]; // PRETA
        } else {
            // Dimensões da imagem não suportadas, fechar imagem e pular para a próxima
            imagem.close(SaveOptions.DONOTSAVECHANGES);
            continue;
        }

            // Obtém o nome completo do arquivo (incluindo a extensão)
            var nomeArquivo = arquivos[i].name;

            // Use expressão regular para extrair os números principais do nome do arquivo
            var match = nomeArquivo.match(/(\d+-\d+)/);

            // Verifica se houve correspondência no nome do arquivo
            if (!match) {
                // Nome do arquivo não corresponde ao padrão esperado, fechar imagem e pular para a próxima
                imagem.close(SaveOptions.DONOTSAVECHANGES);
                continue;
            }

            // Obtém o texto correspondente à expressão regular
            var textoNum = match[0];

            // Obtém o layer de texto
            var textoLayer = imagem.artLayers.add();
            textoLayer.kind = LayerKind.TEXT;

            // Define o texto da numeração
            textoLayer.textItem.contents = textoNum;

            // Define a formatação do texto
            var textoItem = textoLayer.textItem;
            textoItem.color.rgb.red = corRGB[0];
            textoItem.color.rgb.green = corRGB[1];
            textoItem.color.rgb.blue = corRGB[2];
            textoItem.size = tamanhoFonte;

            // Define a posição do texto
            var margemEsquerda = 20;
            var margemInferior = 20;
            textoItem.position = Array(margemEsquerda, imagem.height - margemInferior);

            // Salva a imagem em formato JPEG com qualidade máxima e substitui o arquivo anterior
            var caminhoSalvo = new File(pastaOrigem + "/" + nomeArquivo);
            var opcoesSalvar = new JPEGSaveOptions();
            opcoesSalvar.quality = 12; // Qualidade máxima (0 a 12, onde 12 é a máxima)
            imagem.saveAs(caminhoSalvo, opcoesSalvar, true);

            // Fecha a imagem sem salvar alterações na original
            imagem.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
}

// Chamar a função para processar as imagens com diferentes configurações ao iniciar o script
processarImagensComDiferentesConfiguracoes();