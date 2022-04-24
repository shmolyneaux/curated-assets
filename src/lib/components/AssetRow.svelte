<script>
    import { fly, fade, slide } from 'svelte/transition';
    import { db } from "$lib/db.js";
    import AssetThumbnail from '$lib/components/AssetThumbnail.svelte';

    export let asset;

    let assetName = asset.name;
    let previewUrl = asset.thumbnail;
    let downloadUrl = asset.assets[0];
    let tags = asset.tags;
    let creatorId = asset.creator_id;
    let licenseId = asset.license_id;
    let imageIdx = 0;

    let showDetails = false;
    let clipboardStatusText = "";

    let showPreviewModal = false;

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            clipboardStatusText = "Copied!";
        }, function() {
            clipboardStatusText = "Copy Failed!";
        });
    }

    function incrementImage() {
        imageIdx = (imageIdx + 1) % asset.images.length;
    }

    function decrementImage() {
        // Adding asset.images.length ensures we always get the positive remainder
        imageIdx = (imageIdx - 1 + asset.images.length) % asset.images.length;
    }

    function testFoo(e) {
        console.log(e);
    }

    function handleKeyDown(e) {
        if (e.key == "Escape") {
            showPreviewModal = false;
        }
        else if (e.key == "ArrowRight" && showPreviewModal) {
            incrementImage()
        }
        else if (e.key == "ArrowLeft" && showPreviewModal) {
            decrementImage()
        }
    }
</script>

<svelte:window on:keydown={handleKeyDown}/>

<button
    class="flex items-center gap-2 p-2 hover:bg-gray-200 transition-colors ease-out duration-300"
    on:click={() => showDetails = !showDetails}
>
    <AssetThumbnail
        assetPreviewUrl={"/" + previewUrl}
        unhandledClick={() => showPreviewModal = true}
    />
    <div class="grow flex flex-col">
        <div class="flex gap-2 text-3xl text-left">
            <div>
                {assetName}
            </div>
            <div class="shrink flex gap-2">
                {#each tags as tag}
                    <div class="self-center font-mono text-xs rounded-sm p-0.5 hover:bg-gray-300 border border-gray-300 text-gray-500 transition-colors ease-out duration-100">
                        {tag}
                    </div>
                {/each}
            </div>
        </div>
        <div class="self-start p-1">
            <a on:click|stopPropagation={() => {}} href="/{downloadUrl}" class="bg-rose-500 hover:ring-2 ring-rose-600 active:bg-rose-600 text-left text-white p-1 rounded-md transition-all active:transition-none" download>
                Download .{downloadUrl.split('.').at(-1)}
            </a>
        </div>
    </div>
    <div class="flex flex-col items-end">
        <a class="text-rose-600 hover:underline text-right" href="/creator/{creatorId}">
            {db.creators[creatorId].name}
        </a>
        <a class="text-rose-600 hover:underline text-right" href="/license/{licenseId}">
            {db.licenses[licenseId].short_name}
        </a>
    </div>
</button>

{#if showDetails}
    <!--Ideally this would have `transition:slide`, but that seems to break sveltekit...-->
    <div
        class="w-full shadow-inner-lg bg-gray-500 border-t border-gray-100"
    >
        <div class="flex justify-center">
            <div class="flex flex-col gap-2 bg-rose-500 p-2 text-gray-100">
                <div class="">
                    {asset.description}
                </div>
                {#if asset.images.length}
                    <div class="relative bg-rose-600">
                        <button
                            class="absolute left-0 z-10 h-full bg-black opacity-25 hover:opacity-50 active:opacity-75 transition-opacity"
                            on:click={decrementImage}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <button
                            class="absolute right-0 z-10 h-full bg-black opacity-25 hover:opacity-50 active:opacity-75 transition-opacity"
                            on:click={incrementImage}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                        <div class="absolute bottom-0 flex gap-px items-end justify-center z-10 p-0.5 w-full">
                            {#each Array.from(Array(asset.images.length).keys()) as idx}
                                <button
                                    class="imageIndicator"
                                    current={idx == imageIdx || null}
                                    on:click={() => imageIdx = idx}
                                />
                            {/each}
                        </div>
                        <div class="relative flex justify-center h-60 overflow-hidden">
                            {#key imageIdx}
                                <!-- Ideally we'd use `transition:fade="{{ duration: 300 }}"` here but sveltekit has a bug -->
                                <button
                                    class="absolute"
                                    on:click={() => showPreviewModal = true}
                                >
                                    <img
                                        class="h-60"
                                        src={"/" + asset.images[imageIdx]} alt={assetName + " asset preview image " + imageIdx} />
                                </button>
                            {/key}
                        </div>
                    </div>
                {/if}
                {#if asset.sources.length}
                    <div class="flex flex-col">
                        <div>
                            Source:
                        </div>
                        {#each asset.sources as source}
                            <div class="text-sm">
                                <a href={source} class="hover:underline">{source}</a>
                            </div>
                        {/each}
                    </div>
                {/if}
                {#if asset.credit_text}
                    <div>
                        Use the following text to credit the creator:
                        <div class="relative border border-gray-500 rounded-md p-2 bg-gray-300">
                            <div class="absolute top-0 right-0 p-1">
                                <button
                                    on:click={() => copyToClipboard(asset.credit_text)}
                                    class="flex gap-1 p-1 text-gray-500 rounded-sm hover:text-gray-200 hover:bg-gray-400 transition-colors ease-out duration-200"
                                >
                                    {clipboardStatusText}
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                                    </svg>
                                </button>
                            </div>
                            <pre class="text-gray-700">{asset.credit_text}</pre>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
{/if}

{#if showPreviewModal}
    <div
        class="absolute top-0 left-0 z-20 h-screen w-screen flex place-content-center place-items-center text-white bg-black/50"
    >
        <div
            class="relative bg-gray-300 h-5/6 w-5/6"
        >
            <button
                class="absolute left-0 z-30 h-full bg-black/25 hover:bg-black/50 active:bg-rose-900 transition-colors w-10 p-2 active:transition-none"
                on:click={decrementImage}
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
            </button>
            <button
                class="absolute right-0 z-30 h-full bg-black/25 hover:bg-black/50 active:bg-rose-900 transition-colors w-10 p-2 active:transition-none"
                on:click={incrementImage}
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
            </button>
            <div class="absolute bottom-0 flex gap-px items-end justify-center z-30 p-0.5 w-full">
                {#each Array.from(Array(asset.images.length).keys()) as idx}
                    <button
                        class="imageIndicator"
                        current={idx == imageIdx || null}
                        on:click={() => imageIdx = idx}
                    />
                {/each}
            </div>
            <div class="relative h-full flex place-content-center place-items-center">
                <img
                    class=""
                    src={"/" + asset.images[imageIdx]} alt={assetName + " asset preview image " + imageIdx} />
            </div>
        </div>
    </div>
{/if}

<style>
    .imageIndicator {
        @apply rounded-sm h-2 w-6 bg-white transition-all ease-out duration-300 ring-rose-500;
    }

    .imageIndicator:hover {
        @apply bg-rose-500;
    }

    .imageIndicator[current] {
      @apply bg-rose-500 h-3;
    }
</style>
