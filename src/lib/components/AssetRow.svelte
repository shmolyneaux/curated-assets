<script>
    import { db } from "$lib/db.js";
    import AssetThumbnail from '$lib/components/AssetThumbnail.svelte';

    export let assetName;
    export let downloadUrl;
    export let tags;
    export let creatorId;
    export let licenseId;
</script>

<button class="flex items-center gap-2 p-2 hover:bg-gray-200 transition-colors ease-out duration-300">
    <AssetThumbnail assetPreviewUrl={"/" + downloadUrl} />
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
        <div class="self-start">
            <a href="/{downloadUrl}" class="text-left text-rose-600 hover:underline" download>
                Download
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
