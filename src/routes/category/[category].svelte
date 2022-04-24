<script>
    import { db } from "$lib/db.js";
    import { page } from '$app/stores';
    import AssetThumbnail from '$lib/components/AssetThumbnail.svelte';
    import AssetRow from '$lib/components/AssetRow.svelte';
</script>

<div class="flex flex-col gap-2">
    <h1 class="text-5xl p-2">{$page.params.category}</h1>

    <div class="flex flex-col">
    {#each Object.entries(db.assets) as [asset_id, asset]}
        {#if $page.params.category == asset.category}
            <AssetRow
                {asset}
            />
        {/if}
    {/each}
    </div>
</div>
