<template>
    <div id="app">
        <header>
        </header>
        <div class="container">
            <nav>
                <ScrollArea>
                    <div class="p-4">
                        <div v-for="tag in tags" :key="tag.name">
                            <router-link :to="tag.path" class="text-sm">
                                {{ tag.name }}
                            </router-link>
                            <Separator class="my-3" />
                        </div>
                    </div>
                </ScrollArea>
            </nav>
            <main>
                <!-- Vue Router will render routed components here -->
                <router-view></router-view>
            </main>
        </div>
        <footer>
        </footer>
    </div>
</template>


<script setup lang="ts">
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'

const tags = [
    { name: "Home", path: "/" },
    { name: "Management", path: "/management" },
    { name: "Configuration", path: "/configuration" },
    { name: "Recognize", path: "/recognize" },
    { name: "Settings", path: "/settings" },
]
</script>

<style scoped>
.container {
    display: flex;
    padding: 20px;
}

nav {
    position: fixed;
    min-width: 200px;
}

a {
    color: darkslategrey;
}

a:hover {
    text-decoration: underline;
    background-color: transparent;
}

main {
    margin-left: 200px;
    width: 100%;
    max-width: calc(100% - 200px);
    justify-content: center;
    align-items: center;
    padding: 20px;
}
</style>
