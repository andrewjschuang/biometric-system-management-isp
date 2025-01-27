<template>
    <form @submit.prevent="handleSubmit">
        <FormField name="videoSource">
            <FormItem class="form-item">
                <FormLabel>Video Source</FormLabel>
                <FormControl class="form-control">
                    <Input type="text" v-model="videoSource" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <FormField name="tolerance">
            <FormItem class="form-item">
                <FormLabel>Tolerance</FormLabel>
                <FormControl class="form-control">
                    <Input type="number" min="0.1" max="1.0" step="0.1" v-model="tolerance" />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <div class="button-container">
            <Button type="submit">
                Save Changes
            </Button>
        </div>
    </form>
    <Toaster />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import Toaster from '@/components/ui/toast/Toaster.vue'
import { useToast } from '@/components/ui/toast/use-toast'

const { toast } = useToast()

const videoSource = ref<string>('');
const tolerance = ref<number>();

onMounted(async () => {
    try {
        const response = await fetch('http://localhost:5003/api/configuration')
        const data = (await response.json()).data
        videoSource.value = data.video_source
        tolerance.value = data.tolerance
    } catch (e: any) {
        console.error(`Failed to retrieve configuration: ${e.message}`);
        toast({
            title: `Failed to retrieve configuration`,
            variant: 'destructive'
        });
    }
})

const handleSubmit = async () => {
    try {
        const response = await fetch('http://localhost:5003/api/configuration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_source: videoSource.value,
                tolerance: tolerance.value,
            }),
        })
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${response.body}`);
        }
        toast({
            title: `Successfully updated configuration`,
        });
        return await response.json();
    } catch (e: any) {
        console.error(`Failed to update configuration: ${e.message}`);
        toast({
            title: `Failed to update configuration`,
            variant: 'destructive'
        });
    }
}
</script>

<style scoped>
.form-item {
    padding-left: 20px;
    padding-bottom: 10px;
}

.button-container {
    padding-left: 20px;
}
</style>
