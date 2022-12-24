<script>
    import "../app.css";
</script>

<div class="flex items-center p-2 bg-rose-700 text-white gap-6">
    <a href="/" class="text-2xl hover:underline">SHM Assets</a>
    <div class="flex gap-3">
        <a class="hover:underline" href="/">Home</a>
        <a class="hover:underline" href="/about">About</a>
        <a class="hover:underline" href="/contact">Contact</a>
    </div>
</div>

<slot />

<div class="fixed bottom-0 w-full p-2 bg-amber-500 text-white">
    <div class="flex flex-col items-center">
        Work in progress
    </div>
</div>
