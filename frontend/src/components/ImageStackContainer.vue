<template>
    <div class="image-stack">
        <transition-group name="list" tag="div">
            <div v-for="x in images" :key="x.image.id" class="image-container">
                <img :src="x.image.src" class="image" @mouseover="showStaticFrame(x.image.src)"
                    @mouseleave="hideStaticFrame" @click="removeImage(x.image.id, false)" />
                <img :src="x.matched.src" class="matched-image" @mouseover="showStaticFrame(x.matched.src)"
                    @mouseleave="hideStaticFrame" @click="removeImage(x.matched.id, true)" />
            </div>
        </transition-group>
    </div>
</template>

<script setup lang="ts">
const emit = defineEmits(['remove:image', 'static:show', 'static:hide']);

defineProps({
    images: {
        type: Array<any>,
        default: () => [],
    },
    matches: {
        type: Set,
        default: () => new Set(),
    },
});

const removeImage = (id: string, matched: boolean) => {
    emit('remove:image', {
        id,
        matched,
    });
};

const showStaticFrame = (src: string) => {
    emit('static:show', src);
};

const hideStaticFrame = () => {
    emit('static:hide');
};

</script>

<style scoped>
.image-stack {
    margin-top: 20px;
    overflow-x: scroll;
    white-space: nowrap;
}

.image-container {
    display: inline-block;
    margin-right: 10px;
    vertical-align: top;
    position: relative;
    width: 170px;
    border-radius: 10px;
}

.list-enter-active {
    transition: all 0.5s ease;
}

.list-enter-from {
    transform: translateX(100%);
    opacity: 0;
}

.list-leave-active {
    transition: transform 0.5s ease, opacity 0.3s ease;
}

.list-leave {
    transform: scale(1);
    opacity: 1;
}

.list-leave-to {
    transform: scale(1.1);
    opacity: 0;
}

.image-container:first-child {
    margin-left: 5px;
}

.image-container:last-child {
    margin-right: 5px;
}

.image,
.matched-image {
    object-fit: cover;
    display: block;
    flex: 0 0 auto;
    height: 170px;
    border-radius: 10px;
    transition: transform 0.2s ease;
    border: 3px solid transparent;
}

.image:hover {
    border-color: #B22222;
}

.matched-image:hover {
    border-color: #3CB371;
}
</style>
