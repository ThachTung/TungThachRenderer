#version 330 core

        in vec3 color;
        in vec3 normal;
        in vec2 uv;
        in vec3 frag_pos;
        in vec3 cam_pos;
        out vec4 frag_color;

        uniform sampler2D tex;

        struct Light
        {
            vec3 position;
            vec3 color;
        };

        #define NUM_LIGHTS 2
        uniform Light light_data[NUM_LIGHTS];

        vec4 CreateLight(vec3 light_pos, vec3 light_color, vec3 normal, vec3 frag_pos, vec3 view_dir)
        {
            //ambient
            float ambient_strength = 0.1;
            vec3 ambient = ambient_strength * light_color;

            //diffuse
            vec3 norm = normalize(normal);
            vec3 light_dir = normalize(light_pos - frag_pos);
            float diff = max(dot(light_dir, norm), 0.001);
            vec3 diffuse = diff * light_color;

            //specular
            float specular_strength = 1.0;
            vec3 reflect_dir = normalize(-light_dir - norm);
            float spec = pow(max(dot(view_dir, reflect_dir), 0.001), 32);
            vec3 specular = specular_strength * spec * light_color;

            return vec4(color * (diffuse + ambient + specular), 1.0);
        }

        void main()
        {
            vec3 light_color = vec3(1, 0, 0);
            vec3 view_dir = normalize(cam_pos - frag_pos);

            for (int i=0; i < NUM_LIGHTS; i++)
            {
                frag_color += CreateLight(light_data[i].position, light_data[i].color, normal, frag_pos, view_dir);
            }

            frag_color = frag_color * texture(tex, uv);
        }