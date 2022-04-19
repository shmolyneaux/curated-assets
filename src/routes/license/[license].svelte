<script>
    import { db } from "$lib/db.js";
    import { page } from '$app/stores';
    import AssetThumbnail from '$lib/components/AssetThumbnail.svelte';
    import AssetRow from '$lib/components/AssetRow.svelte';

    let licenseId = $page.params.license;
    let info = db.licenses[licenseId];
</script>

<div class="flex flex-col gap-2 p-2">
    <h1 class="text-5xl">
        {info.long_name}
    </h1>
    <div class="text-xl text-gray-400">
        {info.short_name}
    </div>
    <a class="text-rose-600 hover:underline" href={info.link}>License Info</a>
</div>
