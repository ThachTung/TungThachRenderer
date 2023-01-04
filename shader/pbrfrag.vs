#version 330 core

        in vec3 color;
        in vec3 normal;
        in vec2 uv;
        in vec3 frag_pos;
        in vec3 cam_pos;
        out vec4 frag_color;

        uniform sampler2D tex;
        uniform sampler2D tex_roughness;
        uniform sampler2D tex_normal;

        struct Light
        {
            vec3 position;
            vec3 color;
        };

        #define NUM_LIGHTS 2
        uniform Light light_data[NUM_LIGHTS];

        //----------------------- BRDF ---------------------
        //Trowbridge-Reitz GGX NDF
        float DistributionGGX(vec3 N, vec3 H, float roughness)
        {
            float roughness2 = roughness*roughness;
            float NdotH = max(dot(N,H), 0.001);
            float NdotH2 = NdotH * NdotH;

            float denominator = (NdotH2 * (roughness2 - 1.0) + 1.0);
            denominator = 3.14159 * denominator * denominator;

            return roughness2/denominator;
        }

        //Geometry Schlick-GGX
        float GeometrySchlickGGX(float NdotV, float k)
        {
            float denom = NdotV * (1.0 - k) + k;
            return NdotV/denom;
        }
        //Smith's method
        float GeometrySmith(vec3 N, vec3 V, vec3 L, float k)
        {
            float NdotV = max(dot(N,V), 0.001);
            float NdotL = max(dot(N,L), 0.001);
            float ggx1 = GeometrySchlickGGX(NdotV, k); //geometry obstruction
            float ggx2 = GeometrySchlickGGX(NdotL, k); //geometry shadowing
            return ggx1 * ggx2;
        }

        //Fresnel Schlick
        vec3 FresnelSchlick(float cosTheta, vec3 F0)
        {
            return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
        }

        //---------------------------------------------------------------

        void main()
        {
            vec3 light_color = vec3(1, 0, 0);
            vec3 albedo = texture(tex, uv).rgb;
            float roughness = texture(tex_roughness, uv).r;
            float metallic = 0.0;
            vec3 normal_texture = texture(tex, uv).rgb;

            vec3 V = normalize(cam_pos - frag_pos);
            vec3 N = normalize(normal);

            vec3 F0 = vec3(0.04);
            F0 = mix(F0, albedo, metallic);

            vec3 Lo = vec3(0.0);
            for (int i=0; i < NUM_LIGHTS; i++)
            {
                vec3 L = normalize(light_data[i].position - frag_pos);
                vec3 H = normalize(V + L);
                float distance = length(light_data[i].position - frag_pos);
                float attenuation = 1.0 / (distance * distance);
                vec3 radiance = light_data[i].color * attenuation;

                //Cook-Torrance
                float NDF = DistributionGGX(N, H, roughness);
                float G = GeometrySchlickGGX(N, V, L, roughness);
                vec3 F = FresnelSchlick(max(dot(H,V), 0.001), F0);

                vec3 kS = F;
                vec3 kD = vec3(1.0) - kS;
                kD*=1.0 - metallic;

                vec3 numerator = NDF * G * F;
                float denominator = 4.0 * max(dot(N, V), 0.001) * max(dot(N, L), 0.001) + 0.001;
                vec3 specular = numerator/denominator;

                //Radiance Lo
                float NdotL = max(dot(N, L), 0.001);
                Lo += (kD * albedo/3.14159 + specular) * radiance * NdotL;
            }
            vec3 ambient = vec3(0.03) * albedo;
            vec3 color = ambient _ Lo;

            color = color / (color + vec3(1.0));
            color = pow(color, vec3(1.0/2.0));

            frag_color = vec4(color, 1.0);
        }