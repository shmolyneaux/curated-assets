<script>
    import { db } from "$lib/db.js";
</script>

<div class="flex flex-col gap-6 bg-zinc-800 p-6">
    <div class="flex gap-6">
        {#each db['asset_categories'] as category}
            <a href="/category/{category}" class="cursor-pointer rounded-md bg-zinc-700 text-gray-200 hover:bg-zinc-600 p-6 flex-1 flex justify-center">
                {category}
            </a>
        {/each}
    </div>
    <!-- TODO
    <div class="flex justify-center bg-zinc-700 rounded-full p-2">Search</div>
    -->
</div>

<!-- TODO
<div class="flex flex-col gap-6">
    <div class="text-4xl pt-4">Featured Assets</div>

    <div class="flex justify-center gap-6">
        <div class="w-64 h-64 bg-zinc-500">
        </div>
        <div class="w-64 h-64 bg-zinc-500">
        </div>
    </div>
</div>

<div class="flex flex-col gap-6">
    <div class="text-4xl pt-4">Popular Creators</div>

    <div class="flex justify-center gap-6">
        <div class="w-64 h-64 bg-zinc-500">
        </div>
        <div class="w-64 h-64 bg-zinc-500">
        </div>
    </div>
</div>
-->
