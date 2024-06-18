<template>
    <form @submit.prevent="handleSubmit">
        <FormField name="videoSource">
            <FormItem class="form-item">
                <FormLabel>Upload Image</FormLabel>
                <FormControl class="form-control">
                    <Input type="file" placeholder="Image" @change="handlePhotoChange($event)" required />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>
        <div class="button-container">
            <Button type="submit">
                Send
            </Button>
        </div>
    </form>
    <Toaster />
</template>

<script setup lang="ts">
import { ref } from 'vue'
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

const formImage = ref<FormData>(new FormData());
const matches = ref<String[]>([]);

const handlePhotoChange = (event: any) => {
    if (event.target.files?.[0]) {
        formImage.value.append('image', event.target.files[0]);
    }
}

const handleSubmit = async () => {
    try {
        const response = await fetch('http://localhost:5003/api/recognize', {
            method: 'POST',
            body: formImage.value,
        })
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${response.body}`);
        }
        const { data } = await response.json();
        const names = data.join(', ');
        // TODO: show matches decently
        toast({
            title: `Matched with ${names}`,
        });
    } catch (e: any) {
        console.error(`Failed to run recognition: ${e.message}`);
        toast({
            title: `Failed to run recognition`,
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
