<script>
    import { db } from "$lib/db.js";
    import { page } from '$app/stores';
    import AssetThumbnail from '$lib/components/AssetThumbnail.svelte';
    import AssetRow from '$lib/components/AssetRow.svelte';
</script>

<div class="flex flex-col gap-2 p-2">
    <h1 class="text-5xl">{$page.params.category}</h1>

    <div class="flex flex-col">
    {#each Object.entries(db.assets) as [asset_id, asset]}
        <AssetRow assetName={asset.name} downloadUrl={asset.assets[0]} tags={asset.tags} creatorId={asset.creator_id} licenseId={asset.license_id} />
    {/each}
    </div>
</div>
