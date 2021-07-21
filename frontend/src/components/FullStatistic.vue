<template>
    <v-card class="mb-6">
        <v-card-title>
            <h1>Statistic</h1>
        </v-card-title>
        <v-expansion-panels>
            <v-expansion-panel v-for="(item, idx) in 9" :key="idx">
                <v-expansion-panel-header>
                    statistic
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
                    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-card>
</template>