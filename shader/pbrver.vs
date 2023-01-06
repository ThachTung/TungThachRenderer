#version 330 core

        in vec3 position;
        in vec3 vertex_color;
        in vec3 vertex_normal;
        in vec3 vertex_tangent;
        in vec2 vertex_uv;
        uniform mat4 projection_mat;
        uniform mat4 model_mat;
        uniform mat4 view_mat;
        out vec3 color;
        out vec3 normal;
        out vec2 uv;
        out vec3 frag_pos;
        //out vec3 light_pos;
        out vec3 cam_pos;
        out vec3 tangent;

        void main()
        {
            // static light_pos at camera view
            //light_pos = vec3(inverse(model_mat) * vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
            //light_pos = vec3(model_mat * vec4(5, 5, 5, 1));
            //light_pos = vec3(5, 5, 5);

            //camera pos
            cam_pos = vec3(inverse(model_mat) * vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
            gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1.0);
            normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
            frag_pos = vec3(model_mat * vec4(position, 1.0)) ;
            color = vertex_color;
            uv = vertex_uv;
            tangent = vertex_tangent;
        }