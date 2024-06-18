<template>
    <div>
        <VideoContainer :frame="frame" :recording="recording" @update:recording="handleRecordingUpdate" />
        <ImageStackContainer v-if="enableMatchConfirmation" :images="images" :matches="matches"
            @remove:image="removeImage" @static:show="showStaticFrame" @static:hide="hideStaticFrame" />
        <Toaster />
    </div>
</template>

<script setup lang="ts">
import Toaster from '@/components/ui/toast/Toaster.vue'
import { useToast } from '@/components/ui/toast/use-toast'

import ImageStackContainer from '@/components/ImageStackContainer.vue'
import VideoContainer from '@/components/VideoContainer.vue'
import { ref, onMounted, onUnmounted } from 'vue';
import io from 'socket.io-client';

const { toast } = useToast()

let socket: any;
const recording = ref(false);
const frame = ref();
const static_frame = ref(false);
const images = ref<any>([]);
const matches = ref(new Set());
const enableMatchConfirmation = ref()

onMounted(async () => {
    const response = await fetch(`http://localhost:5003/api/settings`)
    const { enable_match_confirmation } = (await response.json()).data
    enableMatchConfirmation.value = enable_match_confirmation

    socket = io('http://localhost:5003');
    socket.on('frame', (data: any) => {
        if (!static_frame.value) {
            frame.value = `data:image/jpeg;base64,${data.frame}`;
        }
    });

    if (enableMatchConfirmation.value) {
        socket.on('match', ({ image, match }: { image: any, match: any }) => {
            addImage(image, match);
        });
    }
});

onUnmounted(async () => {
    socket?.disconnect();
    await stopRecording();
});

const handleRecordingUpdate = async (eventValue: string) => {
    if (eventValue === 'start') {
        await startRecording();
    } else if (eventValue === 'stop') {
        await stopRecording();
    } else {
        console.error('Invalid recording event value', eventValue);
    }
}

const showStaticFrame = (src: string) => {
    static_frame.value = true;
    frame.value = src;
}

const hideStaticFrame = () => {
    static_frame.value = false;
}

const startRecording = async () => {
    if (recording.value === true) return
    try {
        await fetch('http://localhost:5003/start');
        recording.value = true;
    } catch (e: any) {
        console.error(`Failed to connect to socket: ${e.message}`);
        toast({
            title: 'Failed to connect to video',
            variant: 'destructive'
        });
    }
};

const stopRecording = async () => {
    if (recording.value === false) return
    recording.value = false;
    if (!static_frame.value) {
        frame.value = null;
    }
    await fetch('http://localhost:5003/stop');
};

const addImage = (image: any, match: any) => {
    if (!matches.value.has(match.id)) {
        images.value.push({
            matched: {
                id: match.id,
                src: `data:image/jpeg;base64,${match.src}`,
                name: match.name,
            },
            image: {
                id: Math.ceil(Math.random() * 1000000).toString(),
                src: `data:image/jpeg;base64,${image.src}`,
            },
        });
    }
}

const removeImage = ({ id, matched }: { id: string, matched: boolean }) => {
    if (matched) {
        matches.value.add(id)
        images.value = images.value.filter((x: any) => x.matched.id !== id);
        // send match to stop sending
    } else {
        images.value = images.value.filter((x: any) => x.image.id !== id);
    }
}
</script>
