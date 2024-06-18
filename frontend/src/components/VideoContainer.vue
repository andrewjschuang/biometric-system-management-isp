<template>
    <div>
        <img v-if="props.frame" :src="props.frame" class="default-box" :style="{ border }" />
        <div v-else class="default-box" :style="{ border }"></div>
        <div class="button-container">
            <Button style="margin: 5px;" @click="startRecording">Start</Button>
            <Button style="margin: 5px;" @click="stopRecording">Stop</Button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { computed } from 'vue';

const emit = defineEmits(['update:recording', 'update:recording'])

const props = defineProps({
    frame: String,
    recording: Boolean,
});

const border = computed(() => props.recording ? '2px solid red' : '2px solid #f0f0f0');

const startRecording = async () => {
    emit('update:recording', 'start');
};

const stopRecording = async () => {
    emit('update:recording', 'stop');
};
</script>

<style scoped>
.default-box {
    width: 710px;
    height: 400px;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    background-color: #f0f0f0;
    color: #333;
    font-size: 20px;
    border: 3px dashed #ccc;
}

.button-container {
    text-align: center;
    margin-top: 20px;
}
</style>
