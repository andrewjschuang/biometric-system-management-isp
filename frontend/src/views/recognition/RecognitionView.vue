<template>
    <form @submit.prevent="handleSubmit">
        <FormField name="image">
            <FormItem class="form-item">
                <FormLabel>Enviar Foto</FormLabel>
                <FormControl class="form-control">
                    <Input type="file" placeholder="Image" accept="image/*" @change="handlePhotoChange" required />
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>

        <FormField name="event_name">
            <FormItem class="form-item">
                <FormLabel>Selecione o Evento</FormLabel>
                <FormControl class="form-control">
                    <div>
                        <label class="flex items-center">
                            <input type="radio" name="event_name" v-model="eventName" value="culto_pt" required />
                            <span class="ml-2">Culto Português</span>
                        </label>
                        <label class="flex items-center">
                            <input type="radio" name="event_name" v-model="eventName" value="culto_md" />
                            <span class="ml-2">Culto Mandarim</span>
                        </label>
                        <label class="flex items-center">
                            <input type="radio" name="event_name" v-model="eventName" value="culto_tw" />
                            <span class="ml-2">Culto Taiwanês</span>
                        </label>
                        <label class="flex items-center">
                            <input type="radio" name="event_name" v-model="eventName" value="culto_unificado" />
                            <span class="ml-2">Culto Unificado</span>
                        </label>
                        <label class="flex items-center">
                            <input type="radio" name="event_name" v-model="eventName" value="ebd" />
                            <span class="ml-2">EBD</span>
                        </label>
                    </div>
                </FormControl>
                <FormMessage />
            </FormItem>
        </FormField>

        <div class="button-container">
            <Button type="submit">Enviar</Button>
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

const eventName = ref<string>('')
const selectedFile = ref<File | null>(null)

const handlePhotoChange = (event: Event) => {
    const files = (event.target as HTMLInputElement).files
    if (files && files[0]) {
        selectedFile.value = files[0]
    }
}

const handleSubmit = async () => {
    if (!selectedFile.value || !eventName.value) {
        toast({
            title: 'Por favor selecione um evento e envie uma foto.',
            variant: 'destructive'
        })
        return
    }

    const formData = new FormData()
    formData.append('image', selectedFile.value)
    formData.append('event_name', eventName.value)
    formData.append('dry_run', 'false')

    try {
        const response = await fetch('http://localhost:5003/api/recognize', {
            method: 'POST',
            body: formData
        })
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status} - ${response.body}`);
        }
        const { data } = await response.json()
        toast({
            title: `Enviado com sucesso!`,
        })
    } catch (e: any) {
        console.error(`Erro ao enviar imagem: ${e.message}`)
        toast({
            title: `Erro ao enviar imagem`,
            variant: 'destructive'
        })
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
