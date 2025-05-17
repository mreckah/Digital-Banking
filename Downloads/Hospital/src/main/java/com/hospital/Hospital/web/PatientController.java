package com.hospital.Hospital.web;

import com.hospital.Hospital.entities.Patient;
import com.hospital.Hospital.repository.PatientRepo;
import lombok.AllArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;


@Controller
@AllArgsConstructor
public class  PatientController{
    PatientRepo repo;

    @GetMapping("/index")
    public String index(Model model,
                        @RequestParam(name="page",defaultValue = "1") int p,
                        @RequestParam(name="size",defaultValue = "5") int s
                        //@RequestParam(name="keyword",defaultValue = "")String kw
    )
    {
        Page<Patient> page = repo.findAll(PageRequest.of(p,s));
        model.addAttribute("patients", page.getContent());
        model.addAttribute("pages",new int[page.getTotalPages()]);
        model.addAttribute("currentPage",p);
        return "patients";
    }
}
