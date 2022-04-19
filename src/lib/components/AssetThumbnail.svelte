<script>
    export let assetPreviewUrl;

    let audioElement;
    let playbackProgress = 0.0;
    let isPlaying = false;
    let audioLoadedMetadata = false;

    function audioAssetMetadataLoaded(event) {
        audioElement = event.target;
        audioLoadedMetadata = true;
    }

    function audioProgressUpdate(event) {
        playbackProgress = event.target.currentTime / event.target.duration;
    }

    function audioStarted() {
        isPlaying = true;
    }

    function audioStopped() {
        isPlaying = false;
    }

    function togglePlayback() {
        if (audioElement) {
            if (audioElement.paused) {
                audioElement.play()
            } else {
                audioElement.pause()
            }
        }
    }
</script>

<div class="overflow-hidden hover:shadow-2xl transform hover:-translate-y-0.5 h-16 w-16 bg-gray-400 rounded-lg flex text-gray-500 hover:ring-2 active:ring-2 ring-rose-500 hover:text-rose-500 transition-all duration-200">
    {#if assetPreviewUrl.endsWith(".png") || assetPreviewUrl.endsWith(".jpg")}
        <img src={assetPreviewUrl} />
    {:else if assetPreviewUrl.endsWith(".ogg") || assetPreviewUrl.endsWith(".mp3")}
        <button class="relative h-full w-full flex items-center justify-items-center justify-center" on:click={() => togglePlayback()}>
            <audio
                id=testThing
                on:play={audioStarted}
                on:pause={audioStopped}
                on:ended={audioStopped}
                on:timeupdate={audioProgressUpdate}
                on:loadedmetadata={(event) => audioAssetMetadataLoaded(event)}
                preload=metadata
                src={assetPreviewUrl}>
                    Your browser does not support the
                    <code>audio</code> element.
            </audio>
            {#if audioLoadedMetadata}
                <div class="absolute w-16 bottom-0">
                    <div
                        class="h-1 bg-rose-500"
                        style="width: {playbackProgress * 100}%;">
                    </div>
                </div>
                {#if isPlaying}
                    <!-- Stop Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                    </svg>
                {:else}
                    <!-- Play Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                {/if}
            {:else}
                <!-- Clock Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            {/if}
        </button>
    {:else if assetPreviewUrl.endsWith(".gltf")}
        <div class="h-full w-full flex items-center justify-items-center justify-center">
            <!-- Cube Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
        </div>
    {:else}
        <div class="h-full w-full flex items-center justify-items-center justify-center">
            <!-- Document Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
        </div>
    {/if}
</div>

